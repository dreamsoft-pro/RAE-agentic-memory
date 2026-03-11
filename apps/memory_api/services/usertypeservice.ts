javascript
import { BackendAPI } from '@/lib/api';
import { LeanDesignAdvice } from './advice/lean-design-advice';

const UserTypeService = {
  getAll: () => {
    // [BACKEND_ADVICE] Fetch all user types from the backend.
    return BackendAPI.userTypes.getAll().then((data) => data.plain());
  },
  create: (type) => {
    // [BACKEND_ADVICE] Create a new user type in the backend.
    return BackendAPI.userTypes.create(type).then((data) => data.plain());
  },
  update: (type) => {
    // [BACKEND_ADVICE] Update an existing user type in the backend.
    return BackendAPI.userTypes.update(type).then((response) => {
      if (response.response) {
        return response.plain();
      } else {
        throw new Error('Update failed');
      }
    });
  },
  remove: (id, type) => {
    // [BACKEND_ADVICE] Remove a user type from the backend.
    return BackendAPI.userTypes.remove(id, type).then((data) => data.plain());
  }
};

export default UserTypeService;
