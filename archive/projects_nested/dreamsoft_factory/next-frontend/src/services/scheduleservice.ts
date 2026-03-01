javascript
import { API } from '@/lib/api';
import $cacheFactory from 'ng-cache';

const resource = 'schedule';
const cache = $cacheFactory(resource);

export const ScheduleService = {
    sort: (sort) => {
        return new Promise((resolve, reject) => {
            API.patch(`${resource}/sort`, sort)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    },
    
    updateOngoings: (data) => {
        return new Promise((resolve, reject) => {
            // [BACKEND_ADVICE] Heavy logic or complex operations should be handled here.
            API.put(`${resource}/ongoings`, data)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }
};
