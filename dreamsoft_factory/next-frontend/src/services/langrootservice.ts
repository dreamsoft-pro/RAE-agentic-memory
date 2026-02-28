javascript
import { BackendApi } from '@/lib/api';

angular.module('digitalprint.services')
    .service('LangRootService', function ($q, $http, $config) {

        const LangRootService = {};
        const resource = 'langroot';
        const api = new BackendApi($http, $config.API_URL);

        // [BACKEND_ADVICE] Move heavy logic to backend if necessary

        LangRootService.getAll = async () => {
            try {
                const data = await api.get(resource);
                return data;
            } catch (error) {
                throw error;
            }
        };

        LangRootService.getEmpty = async () => {
            try {
                const data = await api.get([resource, 'showEmpty'].join("/"));
                return data;
            } catch (error) {
                throw error;
            }
        };
    });
