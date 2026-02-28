var webpack = require('webpack');
var WebpackDevServer = require('webpack-dev-server');
const path = require("path");
var config = require('./webpack.config.user')(process.argv.slice(2));

const port=80;
new WebpackDevServer({
	hot: true,
	allowedHosts: "all",
	static: {
		directory: path.join(__dirname)
	}
},webpack(config)).listen(port, '0.0.0.0', function (err, result) {

	if (!err) {
		console.log(`server started on ${port}`);
	}else{
		console.error('error',err);
	}

});
