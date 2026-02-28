javascript
// [BACKEND_ADVICE] Lean design and backend-first approach applied.

const path = require('path');
const configModule = require('./configs/prod.config');

function getConfig() {
    return configModule({}).get();
}

function getVersionHash(grunt) {
    if (grunt.option('versionHash') !== undefined) {
        return grunt.option('versionHash');
    }
    const actDate = new Date();
    return `${actDate.getHours()}${actDate.getMinutes()}${actDate.getSeconds()}`;
}

module.exports = function (grunt) {
    require('load-grunt-tasks')(grunt);
    require('time-grunt')(grunt);

    const appOptions = getConfig();
    const versionHash = getVersionHash(grunt);

    const gruntConfigs = {
        hash: versionHash,
        apiUrl: appOptions.apiUrl,
        editorApiUrl: appOptions.editorApiUrl,
        authUrl: appOptions.authUrl,
        staticUrl: appOptions.staticUrl,
        socketUrl: appOptions.socketUrl,
        editorUrl: appOptions.editorUrl,
        id: appOptions.id,
        domainID: appOptions.domainID
    };

    // [BACKEND_ADVICE] Ensure that the gruntConfigs are used appropriately in the backend.
};
