import { build } from 'vite';
import { resolve } from 'node:path';
await build({ configFile: false, build: { emptyOutDir: false, outDir: 'dist-electron', lib: { entry: resolve('electron/main.ts'), formats: ['cjs'], fileName: () => 'main.cjs' }, rollupOptions: { external: ['electron', 'node:child_process', 'node:readline', 'node:path', 'node:fs', 'node:os', 'node:crypto', 'node:net', 'node:async_hooks'] } } });
await build({ configFile: false, build: { emptyOutDir: false, outDir: 'dist-electron', lib: { entry: resolve('electron/preload.ts'), formats: ['cjs'], fileName: () => 'preload.cjs' }, rollupOptions: { external: ['electron'] } } });

await build({ configFile: false, build: { emptyOutDir: false, outDir: 'dist-electron', lib: { entry: resolve('electron/lolaPreload.ts'), formats: ['cjs'], fileName: () => 'lolaPreload.cjs' }, rollupOptions: { external: ['electron'] } } });
