"""Mode profiles only restrict explicitly enabled extensions; they never grant rights."""
MODE_GROUPS={
    'chat':('desktop','skills','mcp'),
    'ide':('project','memory','commands','desktop','skills','mcp'),
    'voice':('assistant','desktop','skills','mcp'),
}


def mode_groups(mode,root,definitions):
    if mode not in MODE_GROUPS:raise ValueError('Неизвестный режим')
    allowed=set(MODE_GROUPS[mode])
    if not root:allowed-={'project','memory','commands'}
    return [(name,tools if name in allowed else []) for name,tools in definitions]
