module.exports = function (appOptions) {

    appOptions.apiUrl = 'http://localhost:8081/api/';
    appOptions.authUrl = 'http://authapp.localhost:8081/';
    appOptions.staticUrl = 'http://localhost:8081/static/';
    appOptions.socketUrl = 'http://authapp.localhost:8081';
    appOptions.editorUrl = 'http://editor.localhost:8081/';
    appOptions.id = '25';
    appOptions.domainID = '2';
    appOptions.gaCodes = {
        'default': '$INDEX_GA_CODE'
    };

    appOptions.mainFolders = {
        'default': 'dist'
    };

    appOptions.seo = {
        'default': {
            title: '$INDEX_SEO_TITLE',
            description: '$INDEX_SEO_DESCRIPTION',
            keywords: '$INDEX_SEO_KEYWORDS'
        },

    };

    appOptions.googleWebTools = {
        'default': '$INDEX_SEARCH_CONSOLE_CODE',

    };

    function get() {
        return appOptions;
    }

    return {
        get: get
    }
};
