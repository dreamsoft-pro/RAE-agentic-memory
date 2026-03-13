var util = require('util');
console.fs = require('../libs/fsconsole.js');
var Controller = require("./Controller.js");

function TokenController(controller) {
    this.socket = controller.socket;
    this.io = controller.io;
    this.name = "TokenController";
    this.socketName = "Token";
}

util.inherits(TokenController, Controller);

TokenController.prototype.readToken = function( token ) {

    console.log('token: ', token);
}

module.exports = TokenController;