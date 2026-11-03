"""Prepare an isolated, pinned Code-OSS runtime; never locates the user's VS Code."""
import argparse,base64,hashlib,json,re,shutil,subprocess,tempfile,zipfile
from pathlib import Path
import httpx

ROOT=Path(__file__).resolve().parents[2]
VERSION='1.143.17232'
BASE='https://github.com/VSCodium/vscodium/releases/download/'+VERSION+'/'
NAME='VSCodium-win32-x64-'+VERSION+'.zip'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true');parser.add_argument('--resources-only',action='store_true');args=parser.parse_args()
    cache=ROOT/'build/neutral-ide';cache.mkdir(parents=True,exist_ok=True)
    archive=cache/NAME
    expected='a1090868af8ac0ac04c22d79fdd02246fa115a78daf38a741d8db06df1753c1d'
    if not args.offline:
        checksum=httpx.get(BASE+NAME+'.sha256',follow_redirects=True,timeout=60);checksum.raise_for_status()
        if checksum.text.split()[0].lower()!=expected:raise ValueError('Upstream SHA256 differs from reviewed pin')
    if not re.fullmatch('[a-f0-9]{64}',expected):raise ValueError('Invalid release SHA256')
    if not archive.exists():
        if args.offline:raise ValueError('Offline archive missing')
        temporary=archive.with_suffix('.part')
        with httpx.stream('GET',BASE+NAME,follow_redirects=True,timeout=120) as response:
            response.raise_for_status()
            with temporary.open('wb') as output:
                for chunk in response.iter_bytes():output.write(chunk)
        if hashlib.sha256(temporary.read_bytes()).hexdigest()!=expected:raise ValueError('Release SHA mismatch')
        temporary.rename(archive)
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=expected:raise ValueError('Cached release SHA mismatch')
    destination=ROOT/'artifacts/neutral-ide/runtime'
    marker=destination/'.neutral-extracted'
    if marker.exists() and marker.read_text(encoding='ascii')!=expected:raise ValueError('Runtime belongs to another pin; use a separate destination for upgrades')
    if not marker.exists():
        destination.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(archive) as z:
            if sum(i.file_size for i in z.infolist())>2_000_000_000:raise ValueError('Unexpected archive size')
            for i in z.infolist():
                if not (destination/i.filename).resolve().is_relative_to(destination.resolve()):raise ValueError('Unsafe ZIP path')
            z.extractall(destination)
        marker.write_text(expected,encoding='ascii')
    product_path=destination/'resources/app/product.json';product=json.loads(product_path.read_text(encoding='utf8'))
    product.update(nameShort='LESHY IDE',nameLong='LESHY IDE',applicationName='neutral-ide',dataFolderName='.neutral-ide',
        win32AppUserModelId='io.neutral.ide',win32DirName='Neutral IDE',win32NameVersion='Neutral IDE',urlProtocol='neutral-ide',
        win32MutexName='neutral-ide',sharedDataFolderName='.neutral-ide-shared',win32RegValueName='NeutralIDE',win32ShellNameShort='Neutral IDE',
        reportIssueUrl='https://github.com/Voklin/Local_Agent/issues',updateUrl='',quality='stable')
    product_path.write_text(json.dumps(product,ensure_ascii=False,indent=2),encoding='utf8')
    original=destination/'VSCodium.exe';exe=destination/'NeutralIDE.exe'
    if original.exists() and not exe.exists():shutil.copy2(original,exe)
    if not exe.is_file():raise ValueError('Missing runtime executable')
    ext=destination/'resources/app/extensions/neutral-agent';shutil.copytree(ROOT/'prototypes/neutral-ide/extension',ext,dirs_exist_ok=True)
    ui=ROOT/'apps/desktop/dist'
    if not (ui/'ide.html').is_file():raise ValueError('Run npm run build before preparing the integrated IDE')
    shutil.copytree(ui/'assets',ext/'ui/assets',dirs_exist_ok=True);shutil.copy2(ui/'ide.html',ext/'ui/ide.html')
    icon=destination/'resources/app/resources/win32/code.ico';shutil.copy2(ROOT/'assets/leshy.ico',icon)
    (destination/'resources/app/out/media/code-icon.svg').write_text((ROOT/'assets/leshy.svg').read_text(encoding='utf-8').replace('fill="currentColor"','fill="#e3c18a" stroke="#20261d" stroke-width="2"'),encoding='utf-8')
    # Branded empty-editor letterpress and restrained native chrome. Idempotent, pinned runtime only.
    media=destination/'resources/app/out/media'
    master=(ROOT/'assets/leshy.svg').read_text(encoding='utf-8')
    (media/'leshy-mark.svg').write_text(master,encoding='utf-8')
    for name,color in [('light','#874329'),('dark','#e3c18a'),('hcLight','#111111'),('hcDark','#ffffff')]:
        (media/('letterpress-'+name+'.svg')).write_text(master.replace('currentColor',color),encoding='utf-8')
    art=ROOT/'apps/desktop/src/assets/leshy'
    shutil.copy2(art/'spot-birch-painted.webp',ext/'ui/spot-birch-painted.webp')
    for motif in ['border','corner','rosette']:shutil.copy2(art/(motif+'.svg'),ext/('ui/motif-'+motif+'.svg'))
    for source,target in [('birch-cutout.webp','leshy-birch.webp'),('diamond.svg','leshy-diamond.svg'),('corner.svg','leshy-corner.svg'),('border.svg','leshy-border.svg'),('forest-depth.webp','leshy-forest.webp'),('autumn-birch.webp','leshy-parchment.webp'),('twilight.webp','leshy-twilight.webp')]:shutil.copy2(art/source,media/target)
    native_css=destination/'resources/app/out/vs/workbench/workbench.desktop.main.css'
    marker='/* LESHY-WORKBENCH-START */'
    original_css=native_css.read_text(encoding='utf-8').split(marker)[0].rstrip()
    native_css.write_text(original_css+'\n'+marker+'\n'+(ROOT/'prototypes/neutral-ide/leshy-workbench.css').read_text(encoding='utf-8'),encoding='utf-8')
    # This distribution intentionally changes one checked resource; preserve the integrity
    # mechanism and all upstream checksums, updating only our rebuilt CSS artifact.
    product['checksums']['vs/workbench/workbench.desktop.main.css']=base64.b64encode(hashlib.sha256(native_css.read_bytes()).digest()).decode('ascii').rstrip('=')
    product_path.write_text(json.dumps(product,ensure_ascii=False,indent=2),encoding='utf-8')
    rcedit=ROOT/'node_modules/electron-winstaller/vendor/rcedit.exe'
    if not rcedit.is_file():raise ValueError('Run npm ci first: rcedit is required for Neutral branding')
    # The bundled legacy rcedit cannot read Cyrillic argv paths; use relative names.
    if not args.resources_only:
      with tempfile.TemporaryDirectory(prefix='neutral-ide-brand-') as temporary:
        staging=Path(temporary);shutil.copy2(exe,staging/'NeutralIDE.exe');shutil.copy2(ROOT/'assets/leshy.ico',staging/'neutral.ico')
        subprocess.run([str(rcedit),'NeutralIDE.exe','--set-icon','neutral.ico','--set-version-string','ProductName','LESHY IDE','--set-version-string','FileDescription','LESHY IDE','--set-version-string','OriginalFilename','NeutralIDE.exe'],cwd=staging,check=True)
        shutil.copy2(staging/'NeutralIDE.exe',exe)
    (destination/'bin/neutral-ide.cmd').write_text('@echo off\nsetlocal\nset ELECTRON_RUN_AS_NODE=1\n"%~dp0..\\NeutralIDE.exe" "%~dp0..\\resources\\app\\out\\cli.js" %*\n',encoding='ascii')
    report={'base':'Code-OSS via VSCodium','version':VERSION,'url':BASE+NAME,'sha256':expected,'exe':str(exe),'upstream_licenses_preserved':True}
    (ROOT/'artifacts/neutral-ide/base-manifest.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(json.dumps(report))


if __name__=='__main__':main()
