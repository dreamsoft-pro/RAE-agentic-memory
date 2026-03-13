module.exports = function (appOptions) {

    appOptions.apiUrl = 'http://localhost:8081/api';
    appOptions.authUrl = 'http://authapp.localhost:8081';
    appOptions.staticUrl = 'http://localhost:8081/static';
    appOptions.socketUrl = 'http://authapp.localhost:8081';
    appOptions.editorUrl = 'http://editor.localhost:8081';

    function get() {
        return appOptions;
    }

    return {
        get: get
    }
};
