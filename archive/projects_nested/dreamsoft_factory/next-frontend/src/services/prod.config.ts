javascript
const apiUrl = 'http://localtest.me/api/';
const authUrl = 'http://authapp.localtest.me/';
const staticUrl = 'http://localtest.me/static/';
const socketUrl = 'http://authapp.localtest.me';
const editorUrl = 'http://editor.localtest.me/';
const id = '25';
const domainID = '2';
const gaCodes = {
    default: '$INDEX_GA_CODE'
};

const mainFolders = {
    default: 'dist'
};

const seo = {
    default: {
        title: '$INDEX_SEO_TITLE',
        description: '$INDEX_SEO_DESCRIPTION',
        keywords: '$INDEX_SEO_KEYWORDS'
    }
};

const googleWebTools = {
    default: '$INDEX_SEARCH_CONSOLE_CODE'
};

// [BACKEND_ADVICE] Heavy logic should be handled in backend services
function get() {
    return { apiUrl, authUrl, staticUrl, socketUrl, editorUrl, id, domainID, gaCodes, mainFolders, seo, googleWebTools };
}

module.exports = {
    get: get
};
