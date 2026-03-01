javascript
import { getApi } from '@/lib/api';

DpCategoryService.getPublic = async () => {
    try {
        const data = await getApi(`${resource}/forViewPublic/1`);
        return data;
    } catch (error) {
        throw error;
    }
};

// [BACKEND_ADVICE] Heavy logic should be handled in the backend service.
DpCategoryService.getOneForView = async (categoryUrl) => {
    try {
        const data = await getApi(`${resource}/oneForView/${categoryUrl}`);
        return data;
    } catch (error) {
        throw error;
    }
};

DpCategoryService.manyForView = async (categories) => {
    var def = $q.defer();
