javascript
import { fetchBackend } from '@/lib/api';

const CountService = {};

const resource = 'dp_calculate';

CountService.reCalculateCart = function(data) {
    return fetchBackend({
        method: 'PATCH',
        url: `${process.env.REACT_APP_API_URL}/${resource}/cartReCalculate`,
        data,
    });
};

CountService.restorePricesCart = function(data) {
    // [BACKEND_ADVICE] Add backend advice if needed
    const def = $q.defer();

    fetchBackend({
        method: 'PATCH',
        url: `${process.env.REACT_APP_API_URL}/${resource}/cartRestorePrices`,
        data,
    }).then(
        (data) => def.resolve(data),
        (error) => def.reject(error)
    );

    return def.promise;
};

export default CountService;
