javascript
const webpack = require('webpack');
const dotenv = require('dotenv');

// Load the .env file
const envConfig = dotenv.config();
if (!envConfig.error) {
    const env = envConfig.parsed;

    // Prepare the variables to be injected into the application
    const envKeys = Object.keys(env).reduce((prev, next) => {
        prev[`process.env.${next}`] = JSON.stringify(env[next]);
        return prev;
    }, {});

    module.exports = {
        plugins: [
            new webpack.DefinePlugin(envKeys)
        ],
        // [BACKEND_ADVICE]******* configurations...
    };
} else {
    throw envConfig.error;
}
