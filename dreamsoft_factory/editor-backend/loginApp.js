/**
 * Logowanie do aplikacji
 */

var express = require('express'),
    mongoose = require('mongoose');
    bodyParser = require('body-parser'),
	app = express(),
	http = require('http').Server(app),
	fs = require('fs'),
	log_stdout = process.stdout,
	util = require('util'),
	log_file = fs.createWriteStream('./debug.log', {flags : 'w'}),
	httpRequest = require('http');

var password = require('./libs/password.js');
console.fs = require('./libs/fsconsole.js');
var Q = require('q');

var mysql = require('mysql');

//var socketio_jwt = require('socketio-jwt');
var jwt = require('jsonwebtoken');
var mainConf = require('./libs/mainConf.js');
var hashing = require('./libs/hashingProof.js');

// @TODO to zmienić na bardziej dynamiczne
var jwt_secret = mainConf.jwt_secret;

var ObjectOption = require('./models/ObjectOption.js').model;
var User = require('./models/User.js').model;
var SecretProof = require('./models/SecretProof.js').model;
var AdminProject = require('./models/AdminProject.js').model;
var ProjectImage = require('./models/ProjectImage.js').model;

var SessionController = require('./controllers/SessionController.js');
try {
	var SessionControllerObject = new SessionController();
} catch(e) {
	console.log('Problem z plikiem kontrolera!');
	console.log( e );
}


var db;

app.use(bodyParser.urlencoded({ extended: true, limit: '100mb' }));
app.use(express.query());

port = 1600;

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, access-token, domainID, secretProof");
  next();
});

var server = http.listen(port, function () {

	var host = 'digitalprint.pro';
	var port = server.address().port;

	console.log('Digitalprint.pro Edytor: http://%s:%s', host, port);

});

function doRequest( companyID ){
	
	var _this = this;
	var def = Q.defer();

	//The url we want is `www.nodejitsu.com:1337/`
	var options = {
	  host: 'api.digitalprint.pro',
	  path: '/test/importUsers?companyID='+companyID,
	  //since we are listening on a custom port, we need to specify it by hand
	  port: '80',
	  //This is what changes the request to a POST request
	  method: 'GET'
	};

	callback = function(response) {
	  var str = ''
	  response.on('data', function (chunk) {
	    str += chunk;
	  });

	  response.on('end', function () {
	    console.log(str);
	    def.resolve(str);
	  });
	}

	var req = httpRequest.request(options, callback);
	req.end();

	/*var client = httpRequest.createClient(80, "http://api.digitalprint.pro/test/importUsers?companyID="+companyID);
	request = client.request();
	request.on('response', function( res ) {
	    res.on('data', function( data ) {
	        console.log( data );
	        def.resolve(data);
	    } );
	} );
	request.end();*/

	return def.promise;
};

function getRootDomain( domainName ){
	var _this = this;
	var def = Q.defer();

	try {

		var connection = mysql.createConnection(mainConf.rootDb);
		connection.connect();
		connection.query('SELECT * FROM `dp_domains` WHERE `dp_domains`.`name` = ? LIMIT 1 ', [domainName], function(err, rows) {
			//console.log(rows);
			connection.end();
			if( err ){
				console.log(err);
				def.reject(err);
			} else {

				if( rows === undefined || rows.length === 0 ){
					def.reject('empty');
				} else {

					def.resolve(rows[0]);

				}

			}

		});


	} catch(err){
		console.log(err);
		def.reject(err);
	}

	return def.promise;
};

function getSuperUser( login, pass ){
	var _this = this;
	var def = Q.defer();
 
	try {

		var connection = mysql.createConnection(mainConf.rootDb);
		connection.connect();

		var hashFromPost = password.hashPass(pass, false);
		//console.log(hashFromPost);

		connection.query('SELECT * FROM `dp_superusers` WHERE `dp_superusers`.`login` = ? AND `pass` = ? LIMIT 1 ', [login,hashFromPost], function(err, rows) {
			//console.log(rows);
			connection.end();
			if( err ){
				console.log(err);
				def.reject(err);
			} else {

				if( rows === undefined || rows.length === 0 ){
					def.reject('empty');
				} else {

					def.resolve(rows[0]);

				}

			}

		});


	} catch(err){
		console.log(err);
		def.reject(err);
	}

	return def.promise;
};


app.get('/api/test', function (req, res) {
	
	
	var pass = req.query.pass;
	var saltOff = true;
	var hash = password.hashPass(pass, saltOff);

	res.json({'res': hash});
	

});

app.post('/api/getHash', function (req, res) {
	//console.log( rea );
	var hash = hashing.hash(req.body.secretProof, req.body.pTime);
	res.json({'res': hash});
});

function getSecretProof(companyID, secretToCheck){
	var _this = this;
	var def = Q.defer();

	try {

		SecretProof.findOne( { 'secretProof': secretToCheck }, function( err, sp  ) {
			if( err ){
				def.reject(err);
			} else {
				//console.log(sp);
				def.resolve( sp );
			}
		});

	} catch(err){
		console.log(err);
		def.reject(err);
	}

	return def.promise;
};

app.post('/api/verify', function (req, res) {

	var token = req.body.token;
	var jwtSecret =  mainConf.jwt_secret;
	//var companyID = req.query.companyID;
	
	var domainName = req.query.domainName;
	if( domainName === undefined ){
		domainName = req.body.domainName;
	}

	//var SecretProof = SecretProof;
	

		//var connection = mysql.createConnection(mainConf.rootDb);
		//connection.connect();

		//connection.query('SELECT * FROM `dp_domains` WHERE name= '+domainName+' LIMIT 1 ', function(err, rows) {
		
		getRootDomain( domainName ).then( function( domainData ) {
			
			try {

				var companyID = domainData.companyID;

				var databaseName = 'editor_'+companyID;
				

				db = mongoose.connect("mongodb://localhost:27017/"+databaseName, function(err) {
					if(err ){
						console.log(err);
						mongoose.disconnect();
						res.status(401).send( {"error": error, 'codeError': '02'} );
					}
				});

				var postSecretProof = req.body.secretProof;
				//var postProofTime = req.body.proofTime;
				//console.log( 'TU: '+jwtSecret );
				var decoded = jwt.verify(token, jwtSecret);
				
				if( decoded === undefined || decoded === null ){
					//res.status(401).send( {"error":} );
					throw  {"error":  'Token błędny!'};
				}



				if( decoded.userID !== undefined && decoded.userID > 0 ){

					
					time = decoded.exp*1000;
			    	var dexp = new Date(time);
			    	var now = new Date();

			    	if( now < dexp ){

			    		if( postSecretProof === null || postSecretProof === undefined || postSecretProof === '' ){
			    			//console.log('TU? <<<<<<<');
			    			throw {"pTime":decoded.proofTime,"error": 'Brak klucza!'};
			    			//console.log( 'TU?????????TU?????????????????????????????????????????????????????????????????' );
			    		}


			    		//console.log(postSecretProof);
			    		//console.log( SecretProof );
			    		var secretToCheck = hashing.unhash(postSecretProof, decoded.proofTime);
			    		//console.log( secretToCheck );
			    		//console.log( SecretProof );
			    		getSecretProof(companyID, secretToCheck).then( function( sp ){

			    			if( sp === null ){
								mongoose.disconnect();
								res.status(401).send( {"error": "Błąd klucza !!!", 'codeError': '02'});
							} else {
								sp.remove( function(err, removed){
									if( err ){
										console.log(err);
										res.status(401).send( {"error": 'Błąd przy usuwaniu klucza!', 'codeError': '03'} );
									} else {
										var newSecretProof = new SecretProof();
										
										newSecretProof.userID = decoded.userID;
										newSecretProof.datetime = new Date();
										newSecretProof.secretProof = hashing.generate(20);
										var timestamp = newSecretProof.datetime.getTime()/1000 | 0;
										//console.log( 'decoded TU: <<<<<<<<<<<<<<<<<<<<<' );
										//console.log(decoded.first_name);
										newSecretProof.save( function( err, saved ) {
											if(err){
												console.log( err );
												res.status(401).send( {"error": 'Błąd przy zapisywaniu klucza!', 'codeError': '04'} );
											} else {
												//var decoded = jwt.verify(token, conf.jwt_secret);
												var profile = {};
												//console.log(decoded.first_name);
								            	profile.first_name = decoded.first_name;
								            	profile.last_name = decoded.last_name;
								            	profile.email = decoded.email;
								            	profile.userID = decoded.userID;
								            	profile.sessionID = decoded.sessionID;
								            	profile.domainID = decoded.domainID;
								            	profile.exp = time()+(60*60*5);
								            	profile.date = Date.now();
								            	var actTime = new Date();
								            	
								            	profile.proofTime = actTime.getTime()/1000 | 0;

								            	//console.log( profile );
								            	// 60*5
								            	var token = jwt.sign(profile, jwtSecret, { expiresInMinutes: 60*5 });

								            	
								            	//console.log( 'sprawdź czas trwania: ' );
								            	//console.log( decoded );
								            	mongoose.disconnect();
								            	//connection.end();
												res.json({token: token,'userID': decoded.userID, 'secretProof': newSecretProof.secretProof,'domainID': profile.domainID });
											}
										});
									}
								});
							}

			    		});

			    	} else {
			    		mongoose.disconnect();
			    		res.status(401).send( {"error": 'Token wygasł!', 'codeError': '05'} );
			    	}
				} else {
					mongoose.disconnect();
					res.status(401).send({"error": 'Token nieprawidłowy!', 'codeError': '06'});
				}

			} catch (err){

				//console.log("TUTUTUUT?");
				mongoose.disconnect();
				if( err.pTime !== undefined ){
					res.status(200).send({"error": "Brak secret proof.", "pTime": err.pTime, 'codeError': '08'});
				} else {
					res.status(401).send({"tokenError": err,"error": "Token jest błędny.", 'codeError': '07'});
				}

			}

		});
});

function login(email, pass, domainID, companyID){
	var _this = this;
	var def = Q.defer();

	var saltOff = false;

	try {

		//console.log(JSON.stringify({'a': '2'}));

		doRequest( companyID ).then( function(requestData) {

			// @TODO to trzeba sprawdzać z bazy danych
			if( companyID === 249 || companyID === 686 ){
				saltOff = true;
			}

			User.findOne({ 'email':  email, $or:[ {'domainID':null}, {'domainID': domainID} ]  }, function( err, _user ) {
				//console.log('User');
		        //console.log(_user);
		        if( err ){
		            console.log(err);
		            def.reject(err);
		        } else {
		        	if( _user === null ){
		        		// próbujemy autoryzować super admina
		        		
		        		getSuperUser( email, pass ).then( function( _superuser ) {

		        			//console.log(_superuser);
		        			var profile = {};
				        	profile.first_name = _superuser.name;
				        	profile.last_name = 'ADMIN';
				        	profile.email = _superuser.login;
				        	profile.userID = _superuser.ID;
				        	profile.date = Date.now();
				        	profile.domainID = domainID;
				        	profile.super = 1;
				        	var actTime = new Date();

				        	SessionControllerObject.add2( profile ).then( function( session ) {
				        		profile.proofTime = actTime.getTime()/1000 | 0;
				        		profile.sessionID = session['sid'];
				        		//console.log( mainConf.jwt_secret );
				        		var token = jwt.sign(profile, mainConf.jwt_secret, { expiresInMinutes: (mainConf.expireTime/60) });
				        		//console.log('token');
				        		//console.log(token);
				        		def.resolve({'token':token,'profile':profile});
				        	});

		        		}).fail( function(err) {
		        			//console.log( err );
		        			def.reject({'error':"Login lub hasło nieprawidłowe!",'response': false});
		        		});
		        		
		        	} else {

		        		//console.log('TU<<<<<?');

		        		var hashFromPost = password.hashPass(pass, saltOff);

		        		//console.log('Hasła: ');
		        		//console.log(pass);
		        		//console.log( hashFromPost );
		        		//console.log( _user.password );

			        	if( hashFromPost !== _user.password ){
			        		def.reject({'error':"Login lub hasło nieprawidłowe!",'response': false});
			        	}

			        	var profile = {};
			        	profile.first_name = _user.first_name;
			        	profile.last_name = _user.last_name;
			        	profile.email = _user.email;
			        	profile.userID = _user.userID;
			        	profile.date = Date.now();
			        	profile.super = 0;
			        	profile.domainID = domainID;
			        	var actTime = new Date();


			        	//console.log(profile);
			        	SessionControllerObject.add2( profile ).then( function( session ) {
			        		profile.proofTime = actTime.getTime()/1000 | 0;
			        		profile.sessionID = session['sid'];
			        		//console.log( mainConf.jwt_secret );
			        		var token = jwt.sign(profile, mainConf.jwt_secret, { expiresInMinutes: 60*5 });
			        		//console.log('token');
			        		//console.log(token);
			        		def.resolve({'token':token,'profile':profile});
			        	}).fail( function(err) {
			        		console.log('Err: ');
			        		console.log(err);
			        		def.reject(err);
			        	});

		        	}
		        	
		        }
		        
		    });
		});

	} catch(err){
		console.log('Err in try: ');
		console.log(err);
		def.reject(err);
	}

	return def.promise;
};

app.get('/api/', function (req, res) {
	res.json({test: 'Test aplikacji logowania'});
});

app.post('/api/login', function (req, res) {

	//console.log(req.body.password);
	var domainName = req.query.domainName;
	if( domainName === undefined ){
		domainName = req.body.domainName;
	}
	//mongoose.disconnect();

	//console.log( req.body );

	function getDbData( companyID ){
		var _this = this;
		var def = Q.defer();

		try {

			var connection = mysql.createConnection(mainConf.vpsDb);
			connection.connect();
			connection.query('SELECT `database`, `dbpass` FROM `users_settings` WHERE ID = ?', [companyID], function(err, rows) {

				connection.end();
				if( err ){
					console.log(err);
					def.reject(err);
				} else {

					if( rows === undefined || rows.length === 0 ){
						def.reject('empty');
					} else {

						def.resolve(rows[0]);

					}

				}

			});


		} catch(err){
			console.log(err);
			def.reject(err);
		}

		return def.promise;
	}

	function getDbUser( companyID ){
		var _this = this;
		var def = Q.defer();

		try {

			var connection = mysql.createConnection(mainConf.vpsDb);
			connection.connect();
			connection.query('SELECT `user` FROM `users` WHERE ID = ? ', [companyID], function(err, rows) {

				connection.end();
				if( err ){
					console.log(err);
					def.reject(err);
				} else {

					if( rows === undefined || rows.length === 0 ){
						def.reject('empty');
					} else {

						def.resolve(rows[0]);

					}

				}

			});


		} catch(err){
			console.log(err);
			def.reject(err);
		}

		return def.promise;
	}

	function getDomain(connectData, domainName){
		var _this = this;
		var def = Q.defer();

		try {

			var connection = mysql.createConnection( connectData );
			connection.connect();
			connection.query('SELECT * FROM `dp_domains` WHERE host = ? ', [domainName], function(err, rows) {

				connection.end();
				if( err ){
					console.log(err);
					def.reject(err);
				} else {

					if( rows === undefined || rows.length === 0 ){
						def.reject('empty');
					} else {

						def.resolve(rows[0]);

					}

				}

			});


		} catch(err){
			console.log(err);
			def.reject(err);
		}

		return def.promise;
	}

	try {

		getRootDomain( domainName ).then( function( domainData ) {
			var companyID = domainData['companyID'];

			getDbUser( companyID ).then( function( userName ) {

				if( companyID == 115 ){
					console.log( 'login: '+req.body.password );
					console.log( 'hasło: '+req.body.email );
				}
				

				getDbData( companyID ).then( function( dbData ) {

					//console.log(companyID);
					
					var connectData = { host: 'localhost',
									    user: 'v_'+userName['user'],
									    password: dbData['dbpass'],
									    database : dbData['database'] };

					getDomain(connectData, domainName, companyID).then( function( domainData ) {

						//console.log( req.body.password );
						//console.log( req.body.email );
						//console.log( domainName );

						if( !req.body.password || !req.body.email || !domainName ){
							res.status(400).send({'error': 'Wypełnij dane logowania!', 'data': req.body.toString()});
						} else {

							//console.log('ready state: ');
							if( mongoose.connection.readyState ){
								mongoose.disconnect();
							}

							var databaseName = 'editor_'+companyID;

							db = mongoose.connect("mongodb://localhost:27017/"+databaseName, function(err) {
								if( err ){
									console.log(err);
									mongoose.disconnect();
									res.status(401).send( {"error": error, 'codeError': '02'} );
								}
							});


							var domainID = domainData['ID'];
							//console.log('tu?');
							var loginUser = login(req.body.email, req.body.password, domainID, companyID);
							loginUser.then( function (loginData){

								var newSecretProof = new SecretProof();

								newSecretProof.userID = loginData['profile'].userID;
								newSecretProof.datetime = new Date();
								newSecretProof.secretProof = hashing.generate(20);
								var timestamp = newSecretProof.datetime.getTime()/1000 | 0;

								newSecretProof.save( function( err, saved ) {
									if(err){
										//mongoose.disconnect();
										console.log( err );
										//console.log('Tu1');
									} else {

										mongoose.disconnect();
										var user = { firstname: loginData['profile'].first_name, lastname: loginData['profile'].last_name, mail: loginData['profile'].email };
										res.json({token: loginData.token,'userID': loginData['profile'].userID, 'secretProof': newSecretProof.secretProof,'domainID': domainID, 'user': user });
										//console.log('tu2');
									}
								});
							}).fail(function (error) {
								console.log(error);
								//mongoose.disconnect();
								res.status(400).send(error);
							}).fin(function () {
				    			console.log('wykonało się');
				    			//mongoose.disconnect();
							});;
						}

					})

				});
			});

		});
		

	} catch (err){
		//mongoose.disconnect();
		console.log(err);
	}
	
});
