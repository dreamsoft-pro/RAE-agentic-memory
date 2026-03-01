var util = require('util');
console.fs = require('../libs/fsconsole.js');

var UploadController = require('../controllers/UploadController.js');
var config = require('../confs/main.js');
var Controller = require("../controllers/Controller.js");
var AdminProject = require('../models/AdminProject.js').model;
//var ComplexAdminProject = require('../models/ComplexAdminProject.js').model;
var ProductType = require('../models/ProductType.js').model;
var Format = require('../models/Format.js').model;
var Q = require('q');

function ProductTypeController( controller ) {
	this.socket = controller.socket;
	this.io = controller.io;

    this.name = "ProductTypeController";
    this.socketName = "ProductType";
}

util.inherits(ProductTypeController, Controller);

// on ProductType.setActiveAdminProject
ProductTypeController.prototype.setActiveAdminProject = function(){

	//console.log(this.socketName+'.setActiveAdminProject');
	var socketName =  this.socketName;
	var socket = this.socket;
	socket.on(socketName+'.setActiveAdminProject', function(data) {
		console.log(data);
		console.log('ustawianie aktywnego projektu');

		ProductType.findOne( { typeID : data. typeID} ).populate({
          path: 'AdminProjects',
          match: { active: true }
        }).exec( function( err, productType ){

        	if( err ){

        		console.log( err );

        	}else {

        		console.log( productType );
        		console.log('co znalazlo');

        		if( productType.AdminProjects.length ){

        			productType.AdminProjects[0].active = false;
					productType.AdminProjects[0].save( function( err, saved ){

						AdminProject.findOne({ _id: data.projectID }, function (err, doc){
							if(err || doc === null){
								io.sockets.emit( socketName+'.error', "Nie ma takiego projektu!" );
							}
							var returnObj = {};
							returnObj.name = doc.name;
							returnObj._id = doc._id;
						  	doc.active = true;
							doc.save();

							console.log('wysylam odpowiedz');
							socket.emit( socketName+'.setActiveAdminProject', returnObj );

						});

					});

        		}else {

						AdminProject.findOne({ _id: data.projectID }, function (err, doc){
							if(err || doc === null){
								io.sockets.emit( socketName+'.error', "Nie ma takiego projektu!" );
							}
							var returnObj = {};
							returnObj.name = doc.name;
							returnObj._id = doc._id;
						  	doc.active = true;
							doc.save();

							console.log('wysylam odpowiedz');
							socket.emit( socketName+'.setActiveAdminProject', returnObj );

						});

        		}

        	}

        });

        return;

		AdminProject.findOne({ active: true }, function (err, doc1){

			if(err || doc1 === null){
				io.sockets.emit( 'ProductType.error', "Nie ma takiego projektu!" );
			} else {
				doc1.active = false;
				doc1.save();
			}

			AdminProject.findOne({ _id: data.projectID }, function (err, doc){
				if(err || doc === null){
					io.sockets.emit( socketName+'.error', "Nie ma takiego projektu!" );
				}
				var returnObj = {};
				returnObj.name = doc.name;
				returnObj._id = doc._id;
			  	doc.active = true;
				doc.save();

				console.log('wysylam odpowiedz');
				socket.emit( socketName+'.setActiveAdminProject', returnObj );

			});
		});
	});

};

ProductTypeController._getActiveAdminProjectFormatViews = function( typeID, callback, fallback ) {

	//var existProductType = new ProductType({ typeID: typeID });
	ProductType.findOne({ typeID : typeID }).deepPopulate('AdminProjects AdminProjects.Formats AdminProjects.Formats.Views').exec(function(err, pt) {

		if( err ){

			io.sockets.emit( 'ProductType.AdminProject.error', 'Nie ma typu!' );

		}

		if( pt === null ){

			fallback( null );

		} else {

			if( pt.AdminProjects === undefined ){

				callback( [] );

			} else {

				var activeAdminProject = null;

				for( var i=0; i < pt.AdminProjects.length; i++ ){

					if( pt.AdminProjects[i].active  )
						activeAdminProject = pt.AdminProjects[i];

				}

				callback( activeAdminProject.Formats );

			}
		}

	});

};


ProductTypeController._getActiveAdminProjectFormat = function( typeID, formatID ) {

	var def = Q.defer();

	//var existProductType = new ProductType({ typeID: typeID });
	ProductType.findOne({ typeID : typeID }).deepPopulate('AdminProjects AdminProjects.Formats AdminProjects.Formats.Views').exec(function(err, pt) {

		if( err ){

			console.log( typeID );
			console.log( err );
			io.sockets.emit( 'ProductType.AdminProject.error', 'Nie ma typu!' );

		}



		if( pt === null ){
			console.log( typeID );
			console.log( 'PT jest nulem' );
			def.reject( null );

		} else {

			if( pt.AdminProjects === undefined ){

				callback( [] );

			} else {

				console.log(pt.AdminProjects);

				var activeAdminProject = null;

				for( var i=0; i < pt.AdminProjects.length; i++ ){

					if( pt.AdminProjects[i].active  )
						activeAdminProject = pt.AdminProjects[i];

				}

				console.log( 'activeAdminProject',activeAdminProject );

				var usedFormat = null;
				if(activeAdminProject){
				for( var i=0; i < activeAdminProject.Formats.length; i++ ){

					var format = activeAdminProject.Formats[i];

					if( format.formatID == formatID )
						usedFormat = format;

				}
}
				def.resolve( usedFormat );

			}
		}

	});

	return def.promise;

};


ProductTypeController.prototype.registerNewType = function(){

	var socketName =  this.socketName;
	var socket = this.socket;

	socket.on(socketName+'.registerNewType', function(data) {

		console.log( data );
		console.log('Rejestrowanie nowego typu produktu :)');

	});

}

ProductTypeController.prototype.check = function() {

	var socketName =  this.socketName;
	var socket = this.socket;

	socket.on(socketName+'.check', function(data) {

		console.log('Sprawdzenie typu: ' + data.typeID );
		var existProductType = new ProductType({ typeID: data.typeID });
		existProductType.findByType( function( err, pt ){

			if( err ){

				console.log( err );
				socket.emit( 'Error', { err: err, msg: 'Wystapil problem podczas wczytywania produktu'} );

			}else {

				if( pt )
					socket.emit( 'ProductType.check', { pt } );
				else 
					socket.emit( 'ProductType.check', null );

			}

		});

	});


};

// on ProductType.getAdminProjects
ProductTypeController.prototype.getAdminProjects = function() {
	var socketName =  this.socketName;
	var socket = this.socket;

	socket.on(socketName+'.getAdminProjects', function(data) {

		console.log('getAdminProjects: ', data);

		var existProductType = new ProductType({ typeID: data.typeID });
		existProductType.findByType( function(err, pt) {

			console.log('pt: ', pt);

			if( err ){
				io.sockets.emit( 'ProductType.AdminProject.error', 'Nie ma typu!' );
			}

			if( pt === null ){
				var newProductType = new ProductType({ typeID: data.typeID });
				newProductType.save( function(err, saved){
					if(err){
						console.log(err);
					}
					socket.emit( socketName+'.getAdminProjects', [] );
				});
			} else {
				if( pt.AdminProjects === undefined ){
					console.log('send admin projects: ');
					socket.emit( socketName+'.getAdminProjects', [] );
				} else {
					//console.log(pt.AdminProjects);
					socket.emit( socketName+'.getAdminProjects', pt.AdminProjects );
				}
			}

		});
	});
};

ProductTypeController.prototype.newAdminProject = function() {

	this.socket.on(this.socketName + '.newAdminProject', (data) => {
		// TODO {typeID:data.typeID},
		Format.find((err, typeFormats) => {
			const newAdminProject = new AdminProject({name: data.name, Formats: typeFormats});
			newAdminProject.save((err) => {
				if (err) {
					return this.errorFormat(this.socketName + '.newAdminProject', '')
				}
				var existProductType = new ProductType({typeID: data.typeID});
				existProductType.findOneByType((err, pt) => {
					if (err) {
						return this.errorFormat(this.socketName + '.newAdminProject', '')
					}
					pt.AdminProjects.push(newAdminProject);

					pt.save((err, savedProductType) => {

						if (err) {
							return this.errorFormat(this.socketName + '.newAdminProject', '')
						}
						if (data.URL) {

							UploadController.saveBaseFile(data.URL, config.staticDir + 'adminProjects/' + newAdminProject._id + '.jpg', (url) => {


								newAdminProject.url = url;

								newAdminProject.save((err, savedNewAdminProject) => {

									if (err) {
										return this.errorFormat(this.socketName + '.newAdminProject', '')
									} else {

										ProductType.findOne({typeID: data.typeID}, (err, productType) => {

											if (err) {
												return this.errorFormat(this.socketName + '.newAdminProject', '')
											} else {
												this.socket.emit(this.socketName + '.newAdminProject', productType.AdminProjects || []);

											}

										});

									}

								});

							});

						} else {

							ProductType.findOne({typeID: data.typeID}).deepPopulate('AdminProjects').exec((err, productType) => {

								if (err) {
									return this.errorFormat(this.socketName + '.newAdminProject', '')
								} else {

									this.socket.emit(this.socketName + '.newAdminProject', productType.AdminProjects || []);
									this.socket.emit(this.socketName + '.receiveAdminProject', newAdminProject || {});

								}

							});

						}

					});
				});
			});
		})


	});
};

module.exports = ProductTypeController;
