javascript
import { API } from '@/lib/api';

const NewsletterService = {};

const resource = 'dp_newsletter';

NewsletterService.getAll = (): Promise<any> => {
    return new Promise((resolve, reject) => {
        API.get(resource)
            .then(response => resolve(response.data))
            .catch(error => reject(error));
    });
};

NewsletterService.export = (): Promise<any> => {
    const def = $q.defer();

// [BACKEND_ADVICE] Consider moving heavy logic to backend.
