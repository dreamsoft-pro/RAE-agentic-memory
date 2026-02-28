var util = require('util');
console.fs = require('../libs/fsconsole.js');


var Controller = require("../controllers/Controller.js");
var AdminProject = require('../models/AdminProject.js').model;
var MainTheme = require('../models/MainTheme.js').model;
var EditorText = require('../models/EditorText.js').model;
var View = require('../models/View.js').model;
var Theme = require('../models/Theme.js').model;

//var conf = require('../confs/main.js');

function AdminViewController( controller ) {
	this.socket = controller.socket;
	this.io = controller.io;
    //AdminProjectController.super_.call(this);
    this.name = "AdminViewController";
    this.socketName = "AdminView";
};

util.inherits(AdminViewController, Controller);


AdminViewController.prototype.get = function(){

	var socketName = this.socketName;
	var socket = this.socket;

	socket.on(socketName+'.get', function(data){

		console.log('chcę pobrac konkretny widok');

	});

};


AdminViewController.prototype.removeText = function(){

	var socketName = this.socketName;
	var socket = this.socket;

	socket.on(socketName+'.removeText', function( data ) {

		console.log( data );
		console.log( 'chce usunac tekst z adminview' );

		View.findOne({ _id : data.viewID }).deepPopulate( 'EditorTexts' ).exec( function( err, view ){

			if( err ){

				console.log( err );

			}else {

				var texts = view.EditorTexts;

				texts = _.reject( texts, function( elem ){ 
						
					if( elem._id.toString() == data.textID.toString() ){

						elem.remove( function( err, removedText ){

							if( err ){

								console.log( err );

							}else {

								console.log('obiekt został pomyuslnie usuniety :)))))');

							}

						});

						return true;
					}
					else {

						return false;
					}

				});

				view.EditorTexts = texts;

				view.save( function( err, updatedView ){

					if( err ){

						console.log( err );

					}else {



					}

				});

				console.log( view );
				console.log('ID do usuniecia : ' + data.textID );
				console.log('jaka jest tablica textow');

				//console.log( view );
				//console.log( 'znalazlem widok' );

			}

		});

	});

};


module.exports = AdminViewController;
