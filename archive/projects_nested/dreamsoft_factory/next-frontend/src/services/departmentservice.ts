javascript
import { createDepartment, updateDepartment, deleteDepartment } from '@/lib/api';

const resource = '/departments'; // Assuming this is a constant or derived value

DepartmentService.create = async (data) => {
    try {
        const response = await createDepartment(data);
        return response;
    } catch (error) {
        throw error;
    }
};

DepartmentService.update = async (module) => {
    try {
        const response = await updateDepartment(module.id, module); // Assuming the API requires an ID to identify which department to update
        return response;
    } catch (error) {
        throw error;
    }
};

DepartmentService.remove = async (id) => {
    try {
        const response = await deleteDepartment(id);
        return response;
    } catch (error) {
        throw error;
    }
};
