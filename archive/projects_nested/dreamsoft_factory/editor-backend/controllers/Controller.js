var util = require('util');
console.fs = require('../libs/fsconsole.js');

function Controller(io, socket) {
	this.socket = socket;
	this.localConnectID = null;
	this.setCompanyID = null;
	this.name = null
	this.socketName = null
};

Controller.prototype.setCompanyID = function( companyID ) {
    this.companyID = companyID;
};

Controller.prototype.getCompanyID = function(  ) {
    return this.companyID;
};

Controller.prototype.getSocket = function() {
    return this.socket;
};

Controller.prototype.setLocalConnectID = function( ID ){
	//this.localConnectID = ID;
	this.socket.connectID = ID;
};

Controller.prototype.getLocalConnectID = function() {
	//return this.localConnectID;
	return this.socket.connectID;
};

Controller.prototype.errorFormat = function(eventName, errorMessage) {
	console.fs(`${errorMessage} in ${this.name}`);
	this.socket.emit(eventName, {error:errorMessage});
	return true
};

module.exports = Controller;
