import api from "@/lib/api";

class ModuleService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async deleteModuleKey(moduleID: number, keyID: number): Promise<any> {
        try {
            const response = await api.delete(
                `${this.resource}/${moduleID}/module_keys/${keyID}`
            );
            return response.data.response ? response.data : Promise.reject(response.data);
        } catch (error) {
            throw error;
        }
    }

    async getModuleOptions(moduleID: number, keyID: number): Promise<any> {
        try {
            const response = await api.get(
                `${this.resource}/${moduleID}/module_keys/${keyID}/module_options`
            );
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default ModuleService;