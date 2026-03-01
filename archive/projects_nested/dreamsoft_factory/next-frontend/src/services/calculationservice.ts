javascript
import { createAxiosClient } from '@/lib/api';

const CalculationService = function (groupID, typeID) {
    this.groupID = groupID;
    this.typeID = typeID;
};

CalculationService.prototype.getResource = function () {
    return ['ps_groups', this.groupID, 'ps_types', this.typeID, 'ps_calculate', 'calculatePublic'].join('/');
};

CalculationService.prototype.getVolumes = async function (data) {
    const resource = this.getResource();
    try {
        const response = await createAxiosClient().patch($config.API_URL + resource, data);
        return response.data;
    } catch (error) {
        return Promise.reject(error.response ? error.response.data : error.message);
    }
};

export default CalculationService;
