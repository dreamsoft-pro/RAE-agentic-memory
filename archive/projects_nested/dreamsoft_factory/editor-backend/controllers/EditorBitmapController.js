var util = require('util');
console.fs = require('../libs/fsconsole.js');

var generatorUID = require('../libs/generator.js');
var arraydiff = require('../libs/arraydiff.js');

var _ = require('underscore');
var Q = require('q');

var Controller = require("../controllers/Controller.js");
var EditorBitmap = require('../models/EditorBitmap.js').model;
var View = require('../models/View.js').model;
var ProjectImage = require('../models/ProjectImage.js').model;
var ObjectOption = require('../models/ObjectOption.js').model;

function EditorBitmapController( controller ) {
	this.socket = controller.socket;
	this.io = controller.io;

    this.name = "EditorBitmapController";
    this.socketName = "EditorBitmap";
}

util.inherits(EditorBitmapController, Controller);


EditorBitmapController.prototype.setBorderOptions = function() {
	var socketName = this.socketName;
	var socket = this.socket;

	socket.on(this.socketName+'.setBorderOptions', function(data){

		console.log( data );
		console.log('informacja o ramce, przyszla');

	});

}


EditorBitmapController.prototype._add = function( data ) {

	var def = Q.defer();

	var newEditorBitmap = new EditorBitmap(data);

	newEditorBitmap.save( function(err, saved) {
		if( err ){
			console.log(err);
			def.reject(err);
		} else {
			def.resolve(saved);
		}
	});

	return def.promise;
};

EditorBitmapController.prototype.savePosition = function() {
	var socketName = this.socketName;
	var socket = this.socket;

	socket.on(this.socketName+'.savePosition', function(data) {
		//var actEditorBitmap = new EditorBitmap({ _id: data.editorBitmapID });

		EditorBitmap.findOne({ _id: data.editorBitmapID }, function(err, eb) {
			if( err || eb === null ){
				console.log('Nie znaleziono bitmapy');
				io.sockets.emit( this.socketName+'.error', 'Nie ma EditorBitmap!' );
			} else {
				eb.x = data.x;
				eb.y = data.y;
				eb.save(function(err, seb){
					//console.log(seb);
					if(err){
						console.log('Błąd przesuwania bitmapy: ');
						console.log(err);
					}

					io.sockets.emit( this.socketName+'.savedPosition', { x: seb.x, y: seb.y, uid: seb.uid } );

				});
			}
		});
	});
};

EditorBitmapController.prototype.saveScale = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(this.socketName+'.saveScale', function(data) {
		//console.log(data);
		console.time('scale');
		var actEditorBitmap = new EditorBitmap({ _id: data.editorBitmapID });

		actEditorBitmap.find( function(err, eb) {
			if( err || eb === null ){
				console.log(err);
				io.sockets.emit( this.socketName+'.error', 'Nie ma EditorBitmap!' );
			} else {
				eb.scaleX = data.scaleX;
				eb.scaleY = data.scaleY;
				eb.x = data.x;
				eb.y = data.y;
				eb.save( function(err, saved) {
					if( err ){
						console.log(err);
					}
					//console.log(saved);
					console.timeEnd('scale');
					io.sockets.emit( this.socketName+'.savedScale', { _id: saved._id,x: saved.x, y: saved.y, scaleX: saved.scaleX, scaleY: saved.scaleY } );
				});
			}
		});
	});
};

EditorBitmapController.prototype.saveRotate = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(this.socketName+'.saveRotate', function(data) {
		var actEditorBitmap = new EditorBitmap({ _id: ID });

		actEditorBitmap.find( function(err, eb) {
			if( err || eb === null ){
				console.log(err);
				io.sockets.emit( socketName+'.error', 'Nie ma EditorBitmap!' );
			} else {
				eb.rotation = data.rotation;
				eb.save();
				io.sockets.emit( this.socketName+'.savedRotate', data.ID );
			}
		});
	});
};

EditorBitmapController.prototype.remove = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(socketName+'.remove', function(data) {
		var editorBitmapID = data.editorBitmapID;
		var viewID = data.viewID;

		EditorBitmap.findOne({ _id: editorBitmapID }, function(err, eb) {
			if( err || eb === null ){
				console.log(err);
				io.sockets.emit( socketName+'.error', 'Nie ma EditorBitmap!' );
			} else {
				eb.remove( function(err, removed) {
					if(err){
						console.log(err);
					}
					io.sockets.emit( socketName+'.remove', data );
				});

			}
		});
	});
};

EditorBitmapController._duplicate = function( editorBitmapID ) {

	var def = Q.defer();

	EditorBitmap.findOne({ _id: editorBitmapID }, function( err, editorBitmap ){

		if( err ){



		}
		else {

			var editorBitmapJSON = editorBitmap.toJSON();
			delete editorBitmapJSON._id;

			console.log( editorBitmapJSON );
			console.log( '=============================================================' );

			//var _editorBitmap = new EditorBitmap();

		}

	});

	return def.promise;

};

EditorBitmapController._clone = function( id ){

	var def = Q.defer();

	EditorBitmap.findOne( { _id: id } ).exec( function( err, bitmap ){

		if( err ){
			console.log( err );
		}else {

			var newBitmap = bitmap;
			delete newBitmap._id;

			newBitmap = new EditorBitmap( newBitmap );

			newBitmap.save( function( err, saved ){

				def.resolve( saved );

			} );

		}

	});

	return def.promise;

}

// moze trzeba dac clone to view?
EditorBitmapController.prototype.clone = function(){

	var socketName = this.socketName;
	var socket = this.socket;
	var _editorBitmapController = this;
	socket.on(socketName+'.clone', function(data){

		var viewId = data.viewID;
		var bitmapToClone = data.editorBitmapID;

		console.log( data );

		View.findOne({_id: data.viewID}, function(err, view) {
			if( !err && view !== null ){

				var order = view.EditorBitmaps.length + view.EditorTexts.length;
				EditorBitmap.findOne({ _id : bitmapToClone }, function( err, bitmap ){

					var _bitmap = bitmap.toJSON();

					delete _bitmap._id;
					_bitmap.x += 60;
					_bitmap.y += 60;
					_bitmap.order = order;

					_editorBitmapController.createNew(
						_bitmap,
						function( createdBitmap ){
							view.EditorBitmaps.push( createdBitmap );

							view.save(function(err, _view){
								EditorBitmap.findOne({ _id : createdBitmap._id }, function( err, createdBitmap ){

									var _neb = createdBitmap.toJSON();
									_neb.addTo = 'View'
									_neb.viewID = _view._id;
									console.log('zapisalo');
									io.sockets.emit(socketName+'.added', _neb);

								}).populate('ProjectImage');

							});
						},
						function( err ){

							console.log( err );
							console.log('wystapil problem podczas dupliowania bitmapy');

						}
					);

				});

			}

		});

	});

};

EditorBitmapController.prototype.createNew = function( settings, callback, errorCallback ){

	var newEditorBitmap = new EditorBitmap( settings );
	newEditorBitmap.save(function( err, savedBitmap ){

		if( err ){
			errorCallback( err );
		}
		else {
			callback( savedBitmap );
		}

	});

};


EditorBitmapController.prototype.add = function() {

	var _this = this;
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(socketName+'.add', function(data) {

		var addTo = data.addTo;
		ProjectImage.findOne({"uid": data.projectImageUID}, function(err, pi){
			if( !err && pi !== null ){

				var ebData = data;
				ebData.uid = generatorUID();
				ebData.ProjectImage = pi;

				_this.createNew(
					ebData,
					function( savedBitmap ){

						if( addTo == 'View' ){
							View.findOne({_id: data.addToId}, function(err, view) {
								if( !err && view !== null ){
									view.EditorBitmaps.push(savedBitmap);
									ebData.viewID = data.viewID;
									view.save(function(err, eb){
										//console.log(ebData);
										console.log( 'wysylaaaaam :)' );
										var _savedBitmap = savedBitmap.toJSON();
										_savedBitmap.ProjectImage = pi;
										_savedBitmap.addTo = data.addTo;
										_savedBitmap.addToId = data.addToId;
										_savedBitmap.viewID = data.addToId;
										io.sockets.emit(socketName+'.added', _savedBitmap);

									});
								}
							});
						} else if( addTo == 'optionalBitmap'){
							EditorBitmap.findOne({_id: data.addToId}, function(err, eb) {
								if(err){
									console.log(err);
								}
								if(eb !== null){

								}
							});
						} else if ( addTo == 'noRef' ){
							io.sockets.emit(socketName+'.added', neb);
						}

					},
					function( err ){
						console.log( err );
						console.log('wystapil error podczas dodawania bitmapy');
					}
				);

			}

		});

	});
};

EditorBitmapController.prototype.addAsOption = function() {

	var socketName = this.socketName;
	var socket = this.socket;
	var _this = this;

	socket.on(socketName+'.addAsOption', function(data) {

		console.log( data );

		function deleteEditorBitmap( ID ) {

			var def = Q.defer();

			console.log( ID );

			EditorBitmap.findOne({_id: ID}, function(err, _eb) {

				if( err ){
					console.log( err );
					def.reject(err);
				} else {

					if( _eb !== null ){

						_eb.remove( function(err, removed){

							if( err ){
								console.log(err);
								console.log( err );
							} else {
								def.resolve( removed );
							}

						});

					}
				}

			});

			return def.promise;
		}

		function deleteOptions( ID ) {

			var def = Q.defer();

			console.log( 'co się chcę usunąć ?' );
			console.log( ID );

			ObjectOption.findOne( {_id: ID}, function( err, _objectOption ){

				if( err ){

					console.log( err );
					def.reject( err );

				} else {

					console.log( '_objectOption: ' );
					console.log( _objectOption );

					if( _objectOption !== null ){

						console.log( ' _objectOption.EditorBitmap:  ' );
						console.log( _objectOption.EditorBitmap );

						if( _objectOption.EditorBitmap === undefined ){

							_objectOption.remove( function( err, removed2 ) {

								if(err){
									def.reject( err );
								} else {
									def.resolve( removed2 );
								}

							});

						} else {
							deleteEditorBitmap( _objectOption.EditorBitmap ).then( function( removed ) {

								_objectOption.remove( function( err, removed2 ) {
									if(err){
										def.reject( err );
									} else {
										def.resolve( removed2 );
									}

								});

							});
						}



					}

				}

			});

			return def.promise;

		}

		var editorBitmapID = data.parentID;
		var options = data.options;
		var adminProjectID = data.adminProjectID;
		var projectImageUID = data.projectImageUID;
		delete data.parentID;
		delete data.options;
		delete data.adminProjectID;
		delete data.projectImageUID;
		data.y = data.pos.y;
		delete data.pos.y;
		data.x = data.pos.x;
		delete data.pos.x;
		data.uid = projectImageUID;
		console.log(' Parent bitmap: ');
		console.log( editorBitmapID );

		function smallPromise(counter, eb, saved){
			if( counter === 0 ){
				io.to('AdminProject:'+adminProjectID).emit(socketName+'.addAsOption', {'parent': eb, 'child': saved} );
			}
		}

		EditorBitmap.findOne({_id: editorBitmapID}, function(err, eb){
			if(err){
				console.log(err);
			} else {
				//var _eb = eb;

				var find = false;
				EditorBitmap.deepPopulate(eb, 'ProjectImage ObjectOptions.EditorBitmap', function (err) {

					if(err){

						console.log(err);

					} else {

						if( eb.ObjectOptions.length > 0 ){
							counter=eb.ObjectOptions.length;
							for(var i=0;i<eb.ObjectOptions.length;i++){

								console.log( 'Equal?: ' );
								console.log( eb.ObjectOptions[i].ids );
								console.log( options );
								options = options.map(Number);
								if( _.isEqual(eb.ObjectOptions[i].ids, options) ){

									var oldOptionID = eb.ObjectOptions[i]._id;

									console.log('_id; ');
									console.log(eb.ObjectOptions[i]._id);

									find = true;
									ProjectImage.findOne({uid: projectImageUID}, function(err, _pi) {
										if( err ){
											console.log(err);
										} else {
											console.log( 'Tworzy się nowa bitmapa <<<<<<<<<<<<<<<<<<<<<<<<' );
											console.log( data );
											//data.ProjectImage = _pi;
											var newEditorBitmap = new EditorBitmap( data );
											newEditorBitmap.ProjectImage = _pi;
											newEditorBitmap.save( function(err, saved) {

												if( err ){
													console.log( err );
												} else {
													var newObjectOptions = new ObjectOption();
													newObjectOptions.ids = options;

													//console.log( 'saved v1:' );

													//console.log( saved );

													newObjectOptions.EditorBitmap = saved;

													console.log( newObjectOptions );

													newObjectOptions.save( function(err, savedObjectOption){

														if(err){
															console.log(err);
														} else {
															eb.ObjectOptions.push(savedObjectOption);
															eb.ObjectOptions = _.reject(eb.ObjectOptions, function(item) {
															    return oldOptionID === item._id; // or some complex logic
															});



															eb.save( function( err, saved2 ) {
																if( err ){
																	console.log( err );
																} else {

																	console.log('o co tu biega: ');
																	console.log( oldOptionID );
																	//console.log( eb.ObjectOptions[i] );
																	//delete eb.ObjectOptions[i];

																	deleteOptions( oldOptionID ).then( function( deleted ) {

																		counter--;
																		smallPromise(counter, eb, saved);

																	});
																	//counter--;
																	//smallPromise(counter, eb, saved);

																}
															});
														}

													});



												}
											});
										}
									});

								} else {
									counter--;
								}
							}
						}

						if( find === false ){


							var newEditorBitmap = new EditorBitmap( data );
							newEditorBitmap.save( function(err, saved) {

								if(err){
									console.log(err);
								} else {

									console.log( ' saved v2:  ' );
									console.log(saved);

									var newObjectOptions = new ObjectOption();
									newObjectOptions.ids = options;
									newObjectOptions.EditorBitmap = saved;

									newObjectOptions.save( function(err, savedObjectOption) {

										if( err ){
											console.log(err);
										} else {

											eb.ObjectOptions.push( savedObjectOption );

											eb.save( function( err, saved2 ) {
												if( err ){
													console.log( err );
												} else {
													console.log('OK@2');
													console.log(saved);
													io.to('AdminProject:'+adminProjectID).emit(socketName+'.addAsOption', {'parent': eb, 'child': saved} );
												}
											});

										}
									});



								}


							});


						}


					}


				});

			}

		}).deepPopulate('ProjectImage ObjectOptions.EditorBitmap');
	});
};

EditorBitmapController.prototype.setBase = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(socketName+'.setBase', function(data) {
		var editorBitmapID = data.editorBitmapID;
		var viewID = data.viewID;
		EditorBitmap.findOne({_id: editorBitmapID}, function(err, eb) {
			if(err){
				console.log(err);
			}
			eb.base = true;
			eb.save( function(err, saveEB){

				if(err){
					console.log(err);
				}
				View.findOne({_id: viewID}, function(err, view){
					if(err){
						console.log(err);
					}
					View.deepPopulate(view, 'EditorBitmaps EditorBitmaps.ProjectImage', function (err,p) {
						var editorBitmaps = [];
						if( view.EditorBitmaps !== undefined && view.EditorBitmaps.length > 0 ){
							for(var i in view.EditorBitmaps){
								//console.log('base: ');
								//console.log(view.EditorBitmaps[i].base);
								if(view.EditorBitmaps[i].base === true){
									editorBitmaps.push(view.EditorBitmaps[i]);
								}
							}
						}
						console.log(editorBitmaps);
						io.sockets.emit(socketName+'.setBase', editorBitmaps);
					});

				}).deepPopulate('EditorBitmaps EditorBitmaps.ProjectImage');

			});
		});
	});
};

EditorBitmapController.prototype.unsetBase = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(socketName+'.unsetBase', function(data) {
		//console.log('unset: ');
		//console.log(data);
		var editorBitmapID = data.editorBitmapID;
		var viewID = data.viewID;
		EditorBitmap.findOne({_id: editorBitmapID}, function(err, eb) {
			if(err){
				console.log(err);
			}
			eb.base = false;
			eb.save( function(err, saveEB){

				if(err){
					console.log(err);
				}
				View.findOne({_id: viewID}, function(err, view){
					if(err){
						console.log(err);
					}
					View.deepPopulate(view, 'EditorBitmaps EditorBitmaps.ProjectImage', function (err,p) {
						var editorBitmaps = [];
						if( view !== undefined && view.EditorBitmaps !== undefined && view.EditorBitmaps.length > 0 ){
							for(var i in view.EditorBitmaps){
								//console.log('base: ');
								//console.log(view.EditorBitmaps[i].base);
								if(view.EditorBitmaps[i].base === true){
									editorBitmaps.push(view.EditorBitmaps[i]);
								}
							}
						}
						io.sockets.emit(socketName+'.unsetBase', editorBitmaps);
					});

				}).deepPopulate('EditorBitmaps EditorBitmaps.ProjectImage');

			});
		});
	});
};

EditorBitmapController.prototype.getAllBase = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(socketName+'.getAllBase', function(data) {
		//console.log(data);
		var viewID = data.viewID;
		View.findOne({_id: viewID}, function(err, view){
			if(err){
				console.log(err);
			}
			View.deepPopulate(view, 'EditorBitmaps EditorBitmaps.ProjectImage', function (err) {
				var editorBitmaps = [];
				if( err ){
					console.log(err);
					return;
				}
				if( view === null ){
					console.log( 'Nie ma widoku: ' );
					return;
				}
				if( view.EditorBitmaps !== null && view.EditorBitmaps !== undefined && view.EditorBitmaps.length > 0 ){
					for(var i in view.EditorBitmaps){
						//console.log('base: ');
						//console.log(view.EditorBitmaps[i].base);
						if(view.EditorBitmaps[i].base === true){
							editorBitmaps.push(view.EditorBitmaps[i]);
						}
					}
				}
				io.sockets.emit(socketName+'.getAllBase', editorBitmaps);
			});

		}).deepPopulate('EditorBitmaps EditorBitmaps.ProjectImage');
	});
};

EditorBitmapController.prototype._setOptions = function( id, options, callback, errorCallback ){

	EditorBitmap.findOne({ _id : id }, function( err, editorBitmap ){

		if( err ){

			errorCallback( err );

		}else {

			for( var key in options ){

				editorBitmap[key] = options[key];

			}

			editorBitmap.save(function( err, savedBitmap ){

				callback( savedBitmap );

			});

		}

	});

};

EditorBitmapController.prototype.setSettings = function(){

	var socketName = this.socketName;
	var socket = this.socket;

	var _this = this;

	socket.on(socketName+'.setSettings', function(data) {

		EditorBitmap.findOne({ _id: data.editorBitmapID }).exec( function( err, bitmap ){

			if( err ){

				console.log( err );
				return false;

			}

			for( var key in data.settings ){

				bitmap[key] = data.settings[key];

			}

			bitmap.save( function( err, saved ){

				if( err ){

					console.log(err);

				}else {



				}

			});

		});


	});

};

EditorBitmapController.prototype.setAttributes = function() {
	var socketName = this.socketName;
	var socket = this.socket;

	var _this = this;

	socket.on(socketName+'.setAttributes', function(data) {

		_this._setOptions(
			data.editorBitmapID,
			data.options,
			function( savedBitmap ){

				io.sockets.emit(socketName+'.setAttributes', savedBitmap );

			},
			function( err ){

				console.log('wystapil problem przy aktualizacji edytor bitmapy');

			}

		);

	});
};

EditorBitmapController.prototype.setOptions = function() {

	var socketName = this.socketName;
	var socket = this.socket;
	var _this = this;

		function deleteRef( ebID ){

		var def = Q.defer();

		EditorBitmap.findOne({_id: ebID}, function(err, _eb) {
			if(err){
				console.log(err);
				def.reject(err);
			}

			if( _eb !== null ){
				if( _eb.ObjectOptions ){
					var list = _eb.ObjectOptions;

					if( list.length > 0 ){
						counter = list.length;
						for (var i = list.length - 1; i >= 0; i--) {
							console.log( list[i] );
							ObjectOption.findOne({_id: list[i]}, function(err, _one) {
								if( err ){
									console.log(err);
									def.reject(err);
								} else {
									if( _one === null ){
										counter--;
										if( counter === 0 ){
											def.resolve(true);
										}
									} else {
										_one.remove( function(err, removed){
											if( err ){
												console.log(err);
												def.reject(err);
											} else {
												counter--;
												if( counter === 0 ){
													def.resolve(true);
												}
											}
										});
									}


								}
							});
						};
					} else {

						def.resolve(false);

					}

				} else {
					def.resolve(false);
				}
			} else {
				def.resolve(false);
			}


		});

		return def.promise;

	};

	socket.on(socketName+'.setOptions', function(data) {

		function smallPromise( counter, eb ){

			if( counter === 0 ){

		    	eb.save( function(err, savedEB) {
					if(err){
						console.log(err);
					}
					var isOK = false;
					if( savedEB !== null ){
						isOK = true;
					}
					io.sockets.emit(socketName+'.setOptions', isOK);
				});
			}
		}

		console.log( ' --=---==----------- setOptions --=========-==-=-=-=-=-=-' );

		var editorBitmapID = data.editorBitmapID;
		var newOptions = data.options;

		deleteRef( editorBitmapID, newOptions ).then( function( removed ){

			EditorBitmap.findOne({_id: editorBitmapID}, function(err, eb){

				console.log(eb);

				counter=newOptions.length;

				console.log( ' ============ A teraz patrzymy ładnie: =================== ' );
				console.log( editorBitmapID );
				console.log( newOptions );
				for(var i=0;i<newOptions.length;i++ ) {

					var newObjectOptions = new ObjectOption({"ids": newOptions[i]});

					newObjectOptions.save( function( err, saved ) {
						eb.ObjectOptions.push(saved);
						counter--;
						smallPromise( counter, eb );
					});

				}


			}).populate('ProjectImage ObjectOptions');

		}).fail( function( error ) {
			console.log('deltaRef Błąd: ');
			console.log( error );
		});

	});
};

EditorBitmapController.prototype.getOptions = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(socketName+'.getOptions', function(data) {

		console.log( ' --=---==----------- getOptions --=========-==-=-=-=-=-=-' );

		var editorBitmapID = data.editorBitmapID;
		EditorBitmap.findOne({_id: editorBitmapID}, function(err, eb){
			if(err){
				console.log(err);
			}
			EditorBitmap.deepPopulate(eb, 'ProjectImage ObjectOptions ObjectOptions.EditorBitmap', function (err) {
				console.log( eb.ObjectOptions );
				if( eb.ObjectOptions !== undefined && eb.ObjectOptions.length > 0 ){
					function smallPromise(counter, result){
						if( counter === 0 ){
							socket.emit(socketName+'.getOptions', result);
						}
					}
					var result = [];
					var counter = eb.ObjectOptions.length;
					//console.log( counter );
					//smallPromise(counter, result);
					for (var i = eb.ObjectOptions.length - 1; i >= 0; i--) {
						console.log( eb.ObjectOptions[i]._id );
						//return;
						ObjectOption.findOne({_id: eb.ObjectOptions[i]._id}, function(err, _oOption) {
							if(err){
								console.log(err);
							} else {
								ObjectOption.deepPopulate(_oOption, 'EditorBitmap EditorBitmap.ProjectImage', function (err, _oo) {
									//console.log(_oo);
									//console.log(_oOption);
									result.push( _oOption );
									counter--;
									smallPromise(counter, result);
								});
							}
						}).deepPopulate('EditorBitmap EditorBitmap.ProjectImage');;
					};
				} else {
					socket.emit(socketName+'.getOptions', []);
				}

			});

		}).deepPopulate('ProjectImage ObjectOptions ObjectOptions.EditorBitmap');
	});
};

EditorBitmapController.prototype.setOption = function() {
	var socketName = this.socketName;
	var socket = this.socket;

	function getEditorBitmap( ID ){

		var def = Q.defer();

		EditorBitmap.findOne({ _id:  ID  }, function( err, _editorBitmap ) {

			if( err ){
				console.log(err);
				def.reject(err);
			}

			def.resolve(_editorBitmap);

		});

		return def.promise;

	}

	socket.on(socketName+'.setOption', function(data) {
		var editorBitmapID = data.editorBitmapID;
		var options = data.options;
		var toSaveEditorBitmapID = data.toSaveEditorBitmapID;
		EditorBitmap.findOne({_id: editorBitmapID}, function(err, eb){
			if(err){
				console.log(err);
			} else {

				var find = false;
				EditorBitmap.deepPopulate(eb, 'ProjectImage ObjectOptions.EditorBitmap', function (err) {

					if(err){

						console.log(err);

					} else {

						if( eb.ObjectOptions.length > 0 ){
							for(var i=0;i<eb.ObjectOptions.length;i++){

								if( _.isEqual(eb.ObjectOptions[i].ids, options) ){

									find = true;
									getEditorBitmap(toSaveEditorBitmapID).then( function( _editorBitmap ) {

										eb.ObjectOptions[i].EditorBitmap = _editorBitmap;
										eb.ObjectOptions[i].save(function(err, saved) {
											if( err ){
												console.log(err);
											} else {
												console.log('ok');
											}
										});

									});
								}
							}
						}

						if( find === false ){
							getEditorBitmap(toSaveEditorBitmapID).then( function( _editorBitmap ) {

								var newObjectOptions = {};
								newObjectOptions.ids = options;
								newObjectOptions.EditorBitmap = _editorBitmap;
								eb.ObjectOptions.push( newObjectOptions );

								eb.save( function(err, saved) {
									if( err ){
										console.log(err);
									} else {
										console.log('ok');
									}

								});

							});
						}


					}


				});

			}

		}).deepPopulate('ProjectImage ObjectOptions.EditorBitmap');
	});
};

EditorBitmapController.prototype.addOptionalBitmap = function() {
	var socketName = this.socketName;
	var socket = this.socket;
	socket.on(socketName+'.addOptionalBitmap', function(data) {
		var editorBitmapID = data.editorBitmapID;

	});
};

EditorBitmapController.prototype.setTransform = function() {

	var socketName = this.socketName;
	var socket = this.socket;

	socket.on(socketName+'.setTransform', function(data) {

		var editorBitmapID = data.editorBitmapID;

		console.log( '-=-=-=-==-=-=--=-=-=-' );
		console.log( editorBitmapID );

		EditorBitmap.findById( editorBitmapID, function( err, _editorBitmap ){

			if( err ){

				console.log( err );

			}
			else {
				if( _editorBitmap === null ){
					console.log('Nie ma bitmapy');
				} else {
					//console.log( _editorBitmap );
					// console.log( 'znalazlem bitmape!' );
					// console.log( data );
					// console.log( 'taki bedzie update' );


					_editorBitmap.x = data.x;
					_editorBitmap.y = data.y;
					_editorBitmap.rotation = data.rotation;
					_editorBitmap.scaleX = data.scaleX;
					_editorBitmap.scaleY = data.scaleY;

					_editorBitmap.save( function( err, updatedBitmap ){

						if( err ){

							console.log( err );

						} else {

							// console.log( updatedBitmap );
							// console.log('bitmapaZaaktualizowana!');

						}

					});
				}

			}

		});

	});

};

EditorBitmapController.prototype.get = function() {

	var socketName = this.socketName;
	var socket = this.socket;

	socket.on(socketName+'.get', function(data) {

		var editorBitmapID = data.editorBitmapID;

		EditorBitmap.findById( editorBitmapID, function( err, _editorBitmap ){

			if( err ){

				console.log( err );

			} else {

				socket.emit(socketName+'.get', _editorBitmap);

			}

		});

	});

};

module.exports = EditorBitmapController;
