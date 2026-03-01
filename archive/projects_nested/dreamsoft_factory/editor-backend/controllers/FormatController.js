var util = require('util');
console.fs = require('../libs/fsconsole.js');
var Q = require('q');
var Controller = require("../controllers/Controller.js");
var Format = require('../models/Format.js').model;
var AdminProject = require('../models/AdminProject.js').model;

function FormatController( controller ) {
	this.socket = controller.socket;
	this.io = controller.io;
    //AdminProjectController.super_.call(this);
    this.name = "FormatController";
    this.socketName = "Format";
};

util.inherits(FormatController, Controller);

FormatController.prototype.update = function(){
	var socketName = this.socketName;
	var socket = this.socket;
	var _this = this;
	socket.on(socketName+'.update', function(data) {

		Format.findOne( { formatID: data.formatID } ).exec( function( err, format ){

			if( format ){

				for( var key in data ){

					format[key] = data[key];

				}

				format.save( function( err, saved ){

					io.sockets.emit( socketName+'.update', saved );

				});

			}

		});

	});

};

FormatController.prototype.add = function() {

	var socketName = this.socketName;
	var socket = this.socket;
	var _this = this;

	socket.on(socketName+'.add', function(data) {

		var format = new Format();

		var projectId = data.projectId;

		delete data.projectId;

		for( var key in data ){
			format[key] = data[key];
		}
		format['external'] = true;

		format.save( function( err, saved ) {

			console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', projectId);

			AdminProject.findOne({ _id: projectId }, function (err, ap){
				if( ap === null ) {
					console.log('Admin project not exist');
				} else {
					ap.Formats.push(saved._id);
					ap.save(function(err, saved) {
						if(err) {
							console.log('Format in Admin project error', err);
						}
						if( saved ) {
							console.log('Format in AdminProject saved!');
						}
					})
				}
			});

			AdminProject.findOneAndUpdate({ _id: projectId }, {$push: {Formats: saved._id}}, { new: true });

			io.sockets.emit( socketName+'.added', saved );

		}, function(err) {
			console.log(err);

			io.sockets.emit( socketName+'.add.error', err );

		});

	});

};

// metody
FormatController.prototype.load = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	var _this = this;
	socket.on(socketName+'.load', function(data) {
		console.time('Format.load');
		//console.log("Data do Format.load: ");
		//console.log(data);
		var adminProjectID = data.adminProjectID;
		var formatID = data.formatID;
		var formatWidth = data.width;
		var formatHeight = data.height;
		var formatSlope = data.slope;
		
		AdminProject.findOne({_id: adminProjectID}, function(err, ap){
			//console.log( ap );
			if(err){
				console.log(err);
			}
			if( ap === undefined ){
				console.log("-=-=-=-=-= Nie ma projektu!");
				io.sockets.emit( socketName+'.error', "Nie ma projektu" );
				return;
			}
			if( ap.Formats !== undefined && ap.Formats !== null && ap.Formats.length > 0 ){

				for(var i=0;i<ap.Formats.length;i++){
					if( ap.Formats[i].formatID == formatID ){
						var actFormatID = ap.Formats[i]._id;
					}
				}
				//console.log(actFormatID);
				if(actFormatID === undefined) {

					if(!formatSlope){
			     	   formatSlope = 0;
			    	}

					var newFormat = new Format({formatID: formatID,width: formatWidth, height: formatHeight, slope: formatSlope});
					newFormat.save( function(err, savedFormat){
						if(err){
							console.log(err);
						}
						AdminProject.findOne({_id: adminProjectID}, function(err, ap){
							if( err ){
								console.log(err);
							}
							ap.Formats.push(savedFormat);
							ap.save( function(err, savedAP) {
								if(err){
									console.log(err);
								}
								//console.log('Zwracany format: ');
								//console.log(savedFormat);
								var actFormatID = savedFormat._id;
								// console.log('Mamy już format ID: ');
								// console.log(actFormatID);
								if( actFormatID !== undefined && actFormatID !== null ){
									var actFormat = new Format({ _id: actFormatID });
									actFormat.findWithPopulate( function (err, ft){
										console.log('-----------------------------------TUTAJ-------------------------------');
										Format.deepPopulate(ft, 'Views Themes', function (err,a) {
											console.log('Case1: ');
											
											ft.ThemesToCopy = [];
											var tmpThemes = [];
											if( ft.Themes !== null ){
												for( var i=0;i<ft.Themes.length;i++ ){
													console.log( ft.Themes[i] );
													if( ft.Themes[i].toCopy === undefined ){
														tmpThemes.push( ft.Themes[i] );
														continue;
													}
													if( ft.Themes[i].toCopy === true ){
														ft.ThemesToCopy.push( ft.Themes[i] );
														//delete ft.Themes[i];
														//i--;
													} else {
														tmpThemes.push( ft.Themes[i] );
													}
												}
												ft.Themes = tmpThemes;
											}

											console.timeEnd('Format.load');
											io.sockets.emit( socketName+'.load', ft );
										});
									});
								}
							});
						});
					});
					//console.log('Po dodaniu: ');
					//console.log(actFormatID);
					
				} else {
					actFormat = new Format({ _id: actFormatID });
					actFormat.findWithPopulate( function (err, ft){
						Format.deepPopulate(ft, 'Views Themes', function (err,a) {
							//console.log('Case2: ');
							ft.ThemesToCopy = [];
							var tmpThemes = [];
							if( ft.Themes !== null ){
								for( var i=0;i<ft.Themes.length;i++ ){
									console.log( ft.Themes[i] );
									if( ft.Themes[i].toCopy === undefined ){
										tmpThemes.push( ft.Themes[i] );
										continue;
									}
									if( ft.Themes[i].toCopy === true ){
										ft.ThemesToCopy.push( ft.Themes[i] );
										//delete ft.Themes[i];
										//i--;
									} else {
										tmpThemes.push( ft.Themes[i] );
									}
								}
								ft.Themes = tmpThemes;
							}
							console.timeEnd('Format.load');
							io.sockets.emit( socketName+'.load', ft );
						});
					});
				}
				
			} else {
				
				if(!formatSlope){
			        formatSlope = 0;
			    }

				var newFormat = new Format({formatID: formatID,width: formatWidth, height: formatHeight, slope: formatSlope});

				console.log( 'ADD FORMAT <<<<<<<<<<<<<<<<<<<<<' );
				console.log( newFormat );

				newFormat.save( function(err, savedFormat){
					if(err){
						console.log(err);
					}
					AdminProject.findOne({_id: adminProjectID}, function(err, ap){
						if( err ){
							console.log(err);
						}
						console.log( savedFormat );
						ap.Formats.push(savedFormat);
						ap.save( function(err, savedAP) {
							if(err){
								console.log(err);
							}
							//console.log('Zwracany format: ');
							//console.log(savedFormat);
							var actFormatID = savedFormat._id;
							//console.log('Mamy już format ID: ');
							//console.log(actFormatID);
							if( actFormatID !== undefined && actFormatID !== null ){
								var actFormat = new Format({ _id: actFormatID });
								actFormat.findWithPopulate( function (err, ft){
									//console.log('-----------------------------------TUTAJ-------------------------------');
									Format.deepPopulate(ft, 'Views Themes', function (err,a) {
										console.log('Case3: ');
										//console.log(ft);
										
										ft.ThemesToCopy = [];
										var tmpThemes = [];
										if( ft.Themes !== null ){
											for( var i=0;i<ft.Themes.length;i++ ){
												console.log( ft.Themes[i] );
												if( ft.Themes[i].toCopy === undefined ){
													tmpThemes.push( ft.Themes[i] );
													continue;
												}
												if( ft.Themes[i].toCopy === true ){
													ft.ThemesToCopy.push( ft.Themes[i] );
													//delete ft.Themes[i];
													//i--;
												} else {
													tmpThemes.push( ft.Themes[i] );
												}
											}
											ft.Themes = tmpThemes;
										}
										
										console.timeEnd('Format.load');
										io.sockets.emit( socketName+'.load', ft );
									});
								});
							}
						});
					});
				});
			}
		}).populate('Formats');
	});
};

FormatController._getViews = function( formatID ){

	var def = Q.defer();

	Format.findOne({ _id : formatID }, function( err, format ){

		if( err ){

			console.log( err );
			def.reject('Wystąpił problem przy pobieraniu widoków formatu');

		}else {

			def.resolve( format.Views );

		}

	}).deepPopulate('Views');

	return def.promise;

};


FormatController.prototype.get = function(){

	var socketName = this.socketName;
	var socket = this.socket;

	socket.on(socketName+'.get', function(data) {
		//console.log('Format.get');
		//console.log(data);
		//return;
		Format.findOne({ _id: data.formatID}).deepPopulate('Themes').exec( function( err, format ){

			if( err ){

				console.log( err );

			}
			else {

				io.sockets.emit( socketName+'.get', format );

			}

		});

	});

};

FormatController.prototype.getByIntID = function() {
	
	var socketName = this.socketName;
	var socket = this.socket;

	socket.on(socketName+'.getByIntID', function(data) {

	    console.log('Pobierz format po ID: ', data.formatID);

		Format.findOne({ formatID: data.formatID}).deepPopulate('Theme View').exec( function( err, format ){

		    console.log('format: ', format);

			if( err ){

				console.log( 'err', err );

			} else {

				io.sockets.emit( socketName+'.getByIntID', format );

			}

		}).catch(function (err) {
            console.log('err: ', err);
        });

	});

};

FormatController.prototype.copy = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(socketName+'.load', function(data) {
		var formatID = data.formatID; 
		var actFormat = new Format({ _id: formatID });
		actFormat.findWithPopulate( function (err, ft){
			Format.deepPopulate(ft, 'Views Themes', function (err,a) {
				//console.log("cały dokument formatu: ");
				//console.log(ft);
				if( ft.Views !== undefined && ft.Views.length > 0 ){
					
				}
			});
		});
	});
};


module.exports = FormatController;
