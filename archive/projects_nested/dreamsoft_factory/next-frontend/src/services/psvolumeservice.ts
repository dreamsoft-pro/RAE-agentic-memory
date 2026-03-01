javascript
import { backendApi } from '@/lib/api';
import { PsTypeService } from './PsTypeService'; // Assuming PsTypeService is a part of the same module or should be imported accordingly

const cache = $cacheFactory('ps_volume');

class VolumeService {
  constructor(groupID, typeID) {
    this.groupID = groupID;
    this.typeID = typeID;
    this.resource = `ps_groups/${groupID}/ps_types/${typeID}/ps_volumes`;
  }

  async getAll(force = false) {
    if (cache.get(this.resource) && !force) {
      return cache.get(this.resource);
    } else {
      try {
        const response = await backendApi.get(this.resource);
        cache.put(this.resource, response.data.plain());
        return response.data.plain();
      } catch (error) {
        throw error;
      }
    }
  }
}

export default function PsVolumeService($q, Restangular, $cacheFactory, $http, $config) {
  return new VolumeService;
}
