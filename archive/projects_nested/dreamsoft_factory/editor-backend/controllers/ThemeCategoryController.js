var util = require('util');
console.fs = require('../libs/fsconsole.js');

var Controller = require("../controllers/Controller.js");
var ThemeCategory = require('../models/ThemeCategory.js').model;

function ThemeCategoryController( controller ) {
	this.socket = controller.socket;
	this.io = controller.io;

    this.name = "ThemeCategoryController";
    this.socketName = "ThemeCategory";
}

util.inherits(ThemeCategoryController, Controller);

// metody
ThemeCategoryController.prototype.add = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(socketName+'.add', function(data){
		//console.log('dodawanie:');
		//console.log(data);
		var newThemeCategory = new ThemeCategory({name: data.name});
		
		newThemeCategory.findOne(function(err, tc){
			if( tc !== null ){
				console.log('Obiekt istnieje');
				socket.emit(socketName+'.exist', tc);
			} else {
				console.log('Dodano.');
				newThemeCategory.save( function(err, last) {
					if(err){
						console.log(err);
					}
					ThemeCategory.find({}, function(err, all) {
						console.log(all);
						io.sockets.emit(socketName+'.added', all);
					});
				});
				
				
			}
		});
	});

};

ThemeCategoryController.prototype.getAll = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(socketName+'.getAll', function(data) {
		//var list = [];
		//console.log('Lista:');
		ThemeCategory.find({}, function(err, tc) {
			console.log(tc);
			if( !err && tc !== null ){
				socket.emit(socketName+'.getAll', tc);
			} else {
				socket.emit(socketName+'.getAll', []);
			}
		});
		
	});
};


module.exports = ThemeCategoryController;
