javascript
import { BackendAPI } from '@/lib/api';

const RoleService = {};

RoleService.getAll = () => {
  const apiClient = new BackendAPI();
  return apiClient.get('roles').then(data => data.plain());
};

RoleService.getRolePerms = id => {
  const apiClient = new BackendAPI();
  return apiClient.get(`roles/${id}/rolePerms`).then(data => data.plain());
};

RoleService.updateSelectedRolePerms = (id, selected) => {
  const apiClient = new BackendAPI();
  return apiClient.post(`roles/${id}/rolePerms`, selected).then(data => {
    if (data.response) {
      return data.plain();
    } else {
      throw new Error('Failed to update role permissions');
    }
  });
};

RoleService.create = group => {
  const apiClient = new BackendAPI();
  // [BACKEND_ADVICE] Add the logic for creating a new role based on the provided group.
};
