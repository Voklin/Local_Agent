"""User-declared check selection; never infer a test command or execute project code."""
import fnmatch
import os

KINDS=('test','lint','types','syntax','custom','diagnostics')


def required_checks(task):
    """Only explicit path selectors can skip checks; linked acceptance criteria stay required."""
    checks=task.get('options',{}).get('checks',[])
    if task.get('options',{}).get('checks_only'):
        task['verification_selection']={'required':[c['id'] for c in checks],'not_applicable':[]}
        return checks
    changed=set(task.get('modified_files',[]))
    for item in task.get('workspace_changes',[]):
        for key in ('path','destination'):
            if isinstance(item.get(key),str):changed.add(item[key])
    linked={c for item in task.get('acceptance',[]) for c in item.get('check_ids',[])}
    selected=[];omitted=[]
    for check in checks:
        patterns=check.get('applies_to',[])
        match=not patterns or not changed or check['id'] in linked
        for path in changed:
            name=path.replace('\\','/')
            if os.name=='nt':name=name.casefold()
            if any(fnmatch.fnmatchcase(name,p.casefold() if os.name=='nt' else p) for p in patterns):match=True
        (selected if match else omitted).append(check)
    task['verification_selection']={'required':[c['id'] for c in selected],'not_applicable':[c['id'] for c in omitted]}
    return selected
