javascript
import { BackendService } from '@/lib/api';
import { CacheProvider } from '@/utils/cache';

const cache = new CacheProvider('ps_realizationTimes');

class RealizationTimeService {
    constructor() {}

    // [BACKEND_ADVICE] Heavy logic for fetching realization times.
    getAll(force) {
        return new Promise((resolve, reject) => {
            if (cache.get('collection') && !force) {
                resolve(cache.get('collection'));
            } else {
                BackendService.getAll('ps_realizationTimes')
                    .then(data => {
                        if (data) {
                            cache.put('collection', data.plain());
                            resolve(data.plain());
                        } else {
                            reject(data);
                        }
                    })
                    .catch(data => {
                        reject(data);
                    });
            }
        });
    }
}

export default new RealizationTimeService();
