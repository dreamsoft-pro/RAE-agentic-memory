javascript
// digitalprint/services/news-service.js
import { BackendApi } from '@/lib/api';
import { createDeferred } from 'utils/promise';

const BACKEND_ADVICE = '// [BACKEND_ADvice]';

class NewsService {
    getResource() {
        return 'dp_news';
    }

    getRss(data) {
        const deferred = createDeferred();

        const resource = this.getResource();
        const url = `${BackendApi().url}/${resource}/rss`;

        BACKEND_ADVICE;
        BackendApi().get(url)
            .then((response) => {
                deferred.resolve(response.data);
            })
            .catch((error) => {
                deferred.reject(error);
            });

        return deferred.promise;
    }
}

export default NewsService;
