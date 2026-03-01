javascript
import { BackendService } from '@/lib/api';
import _ from 'lodash';

const PromotionService = {};

PromotionService.getUploadUrl = () => {
    const uploadResource = ['promotions', 'uploadIcon'];
    return `${BackendService.getApiUrl()}/${uploadResource.join('/')}`;
};

PromotionService.getAll = (force) => {
    if (_.isNull(PromotionService.getAllDef) || force || PromotionService.getAllDef.promise.$$state.status === 1) {
        PromotionService.getAllDef = BackendService.defer();
    } else {
        return PromotionService.getAllDef.promise;
    }
    // [BACKEND_ADVICE] Add logic to fetch promotions from backend here.
    return null; // Placeholder, replace with actual implementation
};

export default PromotionService;

// Initialize deferred object for getAll method
PromotionService.getAllDef = null;

