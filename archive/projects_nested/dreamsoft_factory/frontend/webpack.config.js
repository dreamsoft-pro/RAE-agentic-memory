const webpack = require('webpack');
const dotenv = require('dotenv');

// Load the .env file
const env = dotenv.config().parsed;

// Prepare the variables to be injected into the application
const envKeys = Object.keys(env).reduce((prev, next) => {
    prev[`process.env.${next}`] = JSON.stringify(env[next]);
    return prev;
}, {});

module.exports = {
    plugins: [
        new webpack.DefinePlugin(envKeys)
    ],
    // Other Webpack configurations...
};
