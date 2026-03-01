javascript
import '@/lib/api';
import _ from 'lodash';

const AuctionService = {};

const resource = 'auctions';
const cache = $cacheFactory(resource);
let getAllDef = null;

AuctionService.getAll = function (force) {
    if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
        getAllDef = $q.defer();
    } else {
        return getAllDef.promise;
    }
    
    // [BACKEND_ADVICE] Fetch all auctions logic should be here
    @api.get(resource)
    .then(response => {
        cache.put(resource, response.data);
        getAllDef.resolve(response.data);
    })
    .catch(error => {
        getAllDef.reject(error);
    });

    return getAllDef.promise;
};

export default AuctionService;
