// this is a simple and quick deobfuscator for the chal 4 of flareon 11
const fs = require("fs");

const parser = require("@babel/parser");
const generate = require("@babel/generator").default;
const traverse = require("@babel/traverse").default;
const types = require("@babel/types");

let code = fs.readFileSync('mememaker.js', 'utf-8'); // extracted from the mememaker3000.html file
let ast = parser.parse(code);
let p = console.log;

let u = [ ];

traverse(ast, { // get the big 'u' array
  VariableDeclarator(path) {
    if (!path.node.init)
      return;
    let node = path.node;
    if (!types.isArrayExpression(node.init))
      return;
    if (node.id.name != 'u')
      return;

    let el = node.init.elements;
    for (let e of el)
      u.push(e.value)
  }
})

function a0b(a, b) {
	const c = u;
	return a0b = function (d, e) {
		d = d - 475;
		let f = c[d];
		return f;
	}, a0b(a, b);
}

(function (a, b) {
  const o = a0b,
    c = a;
  while (!![]) {
    try {
      const d = parseInt(o(55277)) / 1 * (parseInt(o(14365)) / 2) + -parseInt(o(68223)) / 3 * (-parseInt(o(90066)) / 4) + parseInt(o(76024)) / 5 + -parseInt(o(73788)) / 6 + parseInt(o(58137)) / 7 * (parseInt(o(59039)) / 8) + -parseInt(o(97668)) / 9 + parseInt(o(26726)) / 10 * (-parseInt(o(11835)) / 11);
      if (d === b) break;else c['push'](c['shift']());
    } catch (e) {
      c['push'](c['shift']());
    }
  }
})(u, 356255);

traverse(ast, { // deobfuscate the array to string calls
  CallExpression(path) {
    let exp = path.node;
    let fname = exp.callee.name;
    if ( fname != 'a0p' &&
         fname != 'q' &&
         fname != 't' &&
         fname != 's')
      return;

    let indx = exp.arguments[0].value;
    path.replaceWith(types.expressionStatement(types.stringLiteral(a0b(indx))));
  }
})

let keep = false;
do {
  traverse(ast, { // append all strings until there are no more strings to append, you feel me?
    BinaryExpression(path) {
      keep = false;
      let node = path.node;

      if (node.operator != '+')
        return;
      if (!types.isStringLiteral(node.left) || !types.isStringLiteral(node.right))
        return;

      let l = node.left.value, r = node.right.value;
      path.replaceWith(types.expressionStatement(types.stringLiteral(l+r)));
      keep = true;
    },
  });
} while(keep);

fs.writeFileSync('final.js', generate(ast).code); // output that bastard
