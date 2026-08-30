/* Pulls the engine straight out of index.html and runs it, so the tests exercise the
   exact bytes that ship. There is no separate engine file to drift from the page. */
'use strict';
var fs = require('fs');
var path = require('path');
var vm = require('vm');

module.exports = function loadEngine() {
  var htmlPath = path.join(__dirname, 'index.html');
  var html = fs.readFileSync(htmlPath, 'utf8');
  var m = html.match(/<script id="famli-engine">([\s\S]*?)<\/script>/);
  if (!m) { throw new Error('No <script id="famli-engine"> block found in index.html'); }
  var sandbox = {};
  sandbox.self = sandbox;            // the engine's UMD wrapper attaches to self
  vm.createContext(sandbox);
  vm.runInContext(m[1], sandbox, { filename: 'index.html#famli-engine' });
  if (!sandbox.FAMLI) { throw new Error('Engine block did not define FAMLI'); }
  return sandbox.FAMLI;
};
