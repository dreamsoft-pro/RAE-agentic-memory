javascript
'use strict';

const api = require('@/lib/api');
const { BackendService } = require('@digitalprint/services/backend');

class ComplexService extends BackendService {
    constructor(groupID, typeID) {
        super();
        this.groupID = groupID;
        this.typeID = typeID;
    }

    getResource() {
        return `ps_groups/${this.groupID}/ps_types/${this.typeID}/ps_complex`;
    }

    getAll() {
        const resource = this.getResource();
        return api.get(`${resource}`).then((response) => response.data, (error) => Promise.reject(error));
    }
}

module.exports = ComplexService;
