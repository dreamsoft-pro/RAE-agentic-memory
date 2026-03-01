javascript
import { backendApiGet } from '@/lib/api';
import _ from 'lodash';

const UserService = {};

const resource = 'users';
const cache = $cacheFactory(resource);
let getAllDef = null;

UserService.getAll = function (force) {
    if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
        getAllDef = $q.defer();
        const cachedData = cache.get(resource);

        if (!force && cachedData) {
            getAllDef.resolve(cachedData);
        } else {
            backendApiGet(resource).then((response) => {
                cache.put(resource, response.data);
                getAllDef.resolve(response.data);
            }, (error) => {
                getAllDef.reject(error);
            });
        }
    }

    return getAllDef.promise;
};

export default angular.module('digitalprint.services').factory('UserService', UserService);
