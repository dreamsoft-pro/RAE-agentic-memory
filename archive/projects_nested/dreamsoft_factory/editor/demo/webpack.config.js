var webpack = require('webpack');
var path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
module.exports = function (options) {
    return {
        mode: "development",
        entry: {
            index: './demo/index.js'
        },

        devtool: 'inline-source-map',
        output: {
            filename: 'demo.js',
            path: path.resolve(__dirname, 'dist')
        },
        plugins: [

            new webpack.DefinePlugin({
                'EDITOR_ENV': {
                    user: true,
                    admin: false,
                    companyID: options[0] || 25,
                    domain: JSON.stringify(options[1] || 'http://localhost'),
                    frameworkUrl: JSON.stringify(options[2] || 'http://localtest.me/api'),
                    backendUrl: JSON.stringify(options[3] || 'http://localhost:1351/api'),
                    authUrl: JSON.stringify(options[4] || 'http://localhost:2600'),
                    staticUrl: JSON.stringify(options[5] || 'http://localtest.me/static/editor'),
                    templatesDir: JSON.stringify('app/'),
                }
            }),
            new HtmlWebpackPlugin({
                chunks: ['index'],
                filename: 'index.html',
                template: './demo.html'
            })
        ],

        module: {

            rules:  [

                {
                    test: /\.js$/,
                    loader: 'babel-loader'
                }

            ]

        }
    }

};
