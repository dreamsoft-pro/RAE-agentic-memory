javascript
import { BackendApi } from '@/lib/api';

const MetaTagService = {};

MetaTagService.resource = 'dp_mainMetaTags';

MetaTagService.getUploadUrl = (resource) => {
    if (resource === undefined) {
        resource = 'dp_mainMetaTags';
    }
    return `${BackendApi.BASE_URL}/${[resource, 'uploadImage'].join('/')}`;
};

MetaTagService.get = (ID) => {
    return new Promise((resolve, reject) => {
        BackendApi.get(`${MetaTagService.resource}/${ID}`)
            .then(response => resolve(response.data))
            .catch(error => reject(error));
    });
};

MetaTagService.add = (metaTag, routeID) => {
    return new Promise((resolve, reject) => {
