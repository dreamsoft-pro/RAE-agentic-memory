var webpack = require('webpack');
var WebpackDevServer = require('webpack-dev-server');
const path = require("path");
var config = require('./demo/webpack.config')(process.argv.slice(2));

const port = 1410
const domain = 'localhost'
new WebpackDevServer({
    hot: true,
    allowedHosts: "all",
    static: {
        directory: path.join(__dirname)
    }
},webpack(config)).listen(port, domain, function (err, result) {

    if (err) {
        console.log(err);
    }

    console.log(`demo listening https://http://localtest.me:${port}`);

});
