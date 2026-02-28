var fs = require('fs');

var arguments = process.argv.slice(2);

var companyID = process.env.COMPANY_ID;
var mainPort = process.env.MAIN_PORT;
var staticDir=process.env.STATIC_DIR;
let staticUrl=process.env.STATIC_URL
let domain=process.env.DOMAIN
let https=process.env.HTTPS=='true'

global.conf = {
	companyID,
	mainPort,
	staticDir: staticDir + companyID + '/',
	staticPath: '/'+companyID,
    staticUrl,
    domain,
    https,
}
module.exports.companyID = companyID;
module.exports.mainPort = mainPort;
module.exports.staticPath = '/'+companyID;
module.exports.staticDir =  staticDir + companyID + '/';
module.exports.staticUrl =  staticUrl;
module.exports.domain =  domain;
module.exports.https =  https;
module.exports.debug_mode = true;
module.exports.salt = process.env.DEFAULT_SALT;
module.exports.jwt_secret = process.env.secretKey;
module.exports.expireTime = (3600*5);

module.exports.mongoHost = process.env.MONGODB_HOST;
module.exports.mongoPort = process.env.MONGODB_PORT;
module.exports.mongoUser = process.env.MONGODB_USER;
module.exports.mongoPwd = process.env.MONGODB_PASS;


module.exports.mkdir = function mkdir(path, root) {

	var dirs = path.split('/'), dir = dirs.shift(), root = (root||'')+dir+'/';

	try { fs.mkdirSync(root); }
	catch (e) {
		//console.log('tutu');
		//dir wasn't made, something went wrong
		if(!fs.statSync(root).isDirectory()) throw new Error(e);
	}

	return !dirs.length||mkdir(dirs.join('/'), root);
};


