import api from "@/lib/api";

class PermissionService {
    static async update(permission: any): Promise<any> {
        const resource = 'aclPermissions';
        try {
            const response = await api.put(`${resource}`, permission);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    }

    static async remove(id: string | number): Promise<any> {
        const resource = ['aclPermissions', id].join("/");
        try {
            const response = await api.delete(resource);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    }
}

export default PermissionService;