javascript
import { BackendApi } from '@/lib/api';

const GroupService = {};

GroupService.getAll = () => {
  // [BACKEND_ADVICE] Heavy logic to fetch all groups.
  return BackendApi.groups.get().then((response) => response.data);
};

GroupService.create = (group) => {
  // [BACKEND_ADvice] Heavy logic for group creation.
  return BackendApi.groups.post(group).then((response) => response.data);
};

GroupService.update = (group) => {
  // [BACKEND_ADVICE] Heavy logic to update a specific group.
  const { id } = group;
  delete group.id;
  return BackendApi.groups[id].put(group)
    .then((response) => response.response ? response.data : Promise.reject());
};

GroupService.remove = (id, group) => {
  // [BACKEND_ADVICE] Heavy logic for removing a specific group.
  return BackendApi.groups[id].remove().then(() => group);
};

export { GroupService };
