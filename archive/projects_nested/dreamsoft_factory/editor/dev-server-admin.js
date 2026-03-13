var webpack = require('webpack');
var WebpackDevServer = require('webpack-dev-server');
var config = require('./webpack.config.admin')(process.argv.slice(2));
const path = require('path');

var port = 80;

new WebpackDevServer({
    hot: true,
    allowedHosts: "all",
    static: {
        directory: path.join(__dirname),
    }
},webpack(config)).listen(port, '0.0.0.0', function (err, result) {

    if (err) {
        console.log(err);
    }

    console.log('Admin dev build listening on ' + port);

});
