"""Syntax-only source symbols with exact UTF-8 byte columns; no execution or semantic reference claims."""
import ast
from pathlib import Path


def extract_symbols(path,text):
    """Parse Python/JS/TS/TSX; failures preserve plain-text search instead of blocking the file."""
    suffix=Path(path).suffix.lower();symbols=[]
    def add(name,kind,start,end,column=0,end_column=0):
        if name and len(symbols)<5000:symbols.append({'name':name[:300],'kind':kind,'start_line':start,'end_line':end,'start_column':column,'end_column':end_column,'precision':'syntax'})
    try:
        if suffix in ('.py','.pyi'):
            tree=ast.parse(text)
            parents={child:parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
            for node in ast.walk(tree):
                if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                    kind='class' if isinstance(node,ast.ClassDef) else 'method' if isinstance(parents.get(node),ast.ClassDef) else 'function'
                    add(node.name,kind,node.lineno,node.end_lineno,node.col_offset,node.end_col_offset)
                elif isinstance(node,(ast.Import,ast.ImportFrom)):
                    for alias in node.names:add(alias.asname or alias.name,'import',node.lineno,node.end_lineno,node.col_offset,node.end_col_offset)
            return symbols,'python-ast'
        if suffix not in ('.js','.jsx','.mjs','.cjs','.ts','.tsx'):return [],'text-only'
        from tree_sitter import Language,Parser
        if suffix in ('.ts','.tsx'):
            import tree_sitter_typescript as grammar
            language=grammar.language_tsx() if suffix=='.tsx' else grammar.language_typescript()
        else:
            import tree_sitter_javascript as grammar
            language=grammar.language()
        parser=Parser(Language(language));parser.timeout_micros=100000
        tree=parser.parse(text.encode('utf-8'));stack=[tree.root_node]
        while stack and len(symbols)<5000:
            node=stack.pop();kind=None;name=node.child_by_field_name('name')
            if node.type in ('function_declaration','generator_function_declaration','method_definition','function_signature','method_signature'):kind='method' if 'method' in node.type else 'function'
            elif node.type in ('class_declaration','interface_declaration','type_alias_declaration','enum_declaration'):kind=node.type.split('_')[0]
            elif node.type=='variable_declarator':
                value=node.child_by_field_name('value')
                if value and value.type in ('arrow_function','function_expression','generator_function'):kind='function'
            elif node.type=='import_statement':kind='import';name=node.child_by_field_name('source')
            elif node.type=='export_statement':
                kind='export';name=node.child_by_field_name('source')
                declaration=node.child_by_field_name('declaration')
                if name is None and declaration is not None:name=declaration.child_by_field_name('name')
                if name is None:name=node
            if kind and name is not None:
                add(name.text.decode('utf-8')[:300],kind,node.start_point.row+1,node.end_point.row+1,node.start_point.column,node.end_point.column)
            stack.extend(reversed(node.named_children))
        return symbols,'tree-sitter-partial' if tree.root_node.has_error else 'tree-sitter'
    except (ImportError,ValueError,SyntaxError,RecursionError,MemoryError,RuntimeError):return [],'parser-unavailable-or-error'
