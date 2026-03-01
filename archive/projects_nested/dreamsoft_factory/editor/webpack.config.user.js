const webpack = require('webpack');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = function (options) {
    return {
        mode: "development",
        entry: {
            index: './app/index.js'
        },

        devtool: 'inline-source-map',
        output: {
            filename: '[name]_editor_user.js',
            path: path.resolve(__dirname, 'app'),
            clean: true, // Ensures the output directory is cleaned before each build
        },
        plugins: [

            new webpack.DefinePlugin({
                EDITOR_ENV: {
                    user: true,
                    admin: false,
                    companyID: options[0] || 25,
                    domain: JSON.stringify(options[1] || 'http://editor.localtest.me'),
                    frameworkUrl: JSON.stringify(options[2] || 'http://localtest.me/api'),
                    backendUrl: JSON.stringify(options[3] || 'http://editor.localtest.me/api'),
                    authUrl: JSON.stringify(options[4] || 'http://authapp.localtest.me'),
                    staticUrl: JSON.stringify(options[5] || 'http://localtest.me/static/editor'),
                    templatesDir: JSON.stringify('app/'),
                    frontendUrl: JSON.stringify(options[6] || 'http://localtest.me'),
                }
            }),
            new HtmlWebpackPlugin({
                chunks: ['index'],
                filename: 'index.html',
                template: 'index.html'
            })

        ],
        module: {
            rules: [
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: 'babel-loader'
                },
                {
                    test: /\.(scss|css)$/,
                    exclude: /node_modules/,
                    use: ['style-loader', 'css-loader', 'sass-loader'],
                }
            ]
        },
        devServer: {
            static: {
                directory: path.join(__dirname, 'app'),
            },
            compress: true,
            port: 9000,
        },
        resolve: {
            extensions: ['.js', '.json'],
        }
    };
};
