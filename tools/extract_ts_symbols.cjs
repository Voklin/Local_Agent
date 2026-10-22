// Reads syntax only; never imports the application or starts Electron.
const fs = require('node:fs');
const ts = require('typescript');

function extract(file) {
  const source = ts.createSourceFile(file, fs.readFileSync(file, 'utf8').replace(/\r\n?/g, '\n'), ts.ScriptTarget.Latest, true);
  const symbols = [];
  function add(node, name, scope, kind, signature) {
    symbols.push({name:[...scope,name].join('.'), leaf:name, kind, signature,
      line:source.getLineAndCharacterOfPosition(node.getStart(source)).line + 1});
  }
  function visit(node, scope = []) {
    if (ts.isFunctionDeclaration(node) && node.name) {
      const name = node.name.text;
      const signature = `${node.modifiers?.some(m => m.kind === ts.SyntaxKind.AsyncKeyword) ? 'async ' : ''}function ${name}(${node.parameters.map(p => p.getText(source)).join(', ')})${node.type ? ': ' + node.type.getText(source) : ''}`;
      add(node,name,scope,'function',signature);
      if (node.body) ts.forEachChild(node.body, child => visit(child,[...scope,name]));
      return;
    }
    if ((ts.isVariableDeclaration(node) || ts.isPropertyAssignment(node)) && node.initializer &&
        (ts.isArrowFunction(node.initializer) || ts.isFunctionExpression(node.initializer))) {
      const name = node.name.getText(source);
      const fn = node.initializer;
      add(node,name,scope,'callback',`${name}(${fn.parameters.map(p => p.getText(source)).join(', ')})${fn.type ? ': ' + fn.type.getText(source) : ''}`);
      ts.forEachChild(fn.body, child => visit(child,[...scope,name]));
      return;
    }
    if (ts.isBinaryExpression(node) && node.operatorToken.kind === ts.SyntaxKind.EqualsToken &&
        (ts.isArrowFunction(node.right) || ts.isFunctionExpression(node.right))) {
      const name=node.left.getText(source), fn=node.right;
      add(node,name,scope,'callback',`${name}(${fn.parameters.map(p => p.getText(source)).join(', ')})`);
      ts.forEachChild(fn.body,child => visit(child,[...scope,name]));
      return;
    }
    if (ts.isTypeAliasDeclaration(node) || ts.isInterfaceDeclaration(node)) {
      add(node,node.name.text,scope,'type',node.getText(source));
      return;
    }
    ts.forEachChild(node,child => visit(child,scope));
  }
  visit(source);
  return {file,symbols};
}

const files = JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(files.map(extract)));
