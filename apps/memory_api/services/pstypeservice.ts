javascript
import { apiCall } from '@/lib/api';

TypeService.getOneByID = async (groupID, typeID) => {
  try {
    const data = await apiCall({
      method: 'GET',
      url: `${process.env.NEXT_PUBLIC_API_URL}/ps_groups/${groupID}/ps_types/oneByID/${typeID}`
    });
    return data;
  } catch (error) {
    throw error;
  }
};

TypeService.cacheRemove = function (groupID) {
  cache.remove(`collection${groupID}`);
};

export default TypeService;
