javascript
'use strict';

const { API_URL_EDITOR } = require('@/config');
const { readCookie } = require('@/services/auth-service');

class PhotoFolderService {
    constructor() {
        this.url = API_URL_EDITOR;
        this.accessTokenName = 'ACCESS_TOKEN_NAME'; // Replace with actual config value
        this.header = {};
        this.header[this.accessTokenName] = readCookie(this.accessTokenName);
    }

    movePhoto(data, fromFolderID, photo) {
        return new Promise((resolve, reject) => {
            const def = { resolve, reject };
            // [BACKEND_ADVICE]
            $http.post(`${this.url}/move-photo`, data, { headers: this.header })
                .then(response => {
                    def.resolve(response.data);
                }, error => {
                    def.reject(error);
                });
        });
    }
}

module.exports = PhotoFolderService;
