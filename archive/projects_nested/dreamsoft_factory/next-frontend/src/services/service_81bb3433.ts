import api from "@/lib/api";

class TypeService {
    private static async fetchType(groupUrl: string, typeUrl: string): Promise<any> {
        const url = `${process.env.API_URL}ps_groups/${groupUrl}/ps_types/oneForView/${typeUrl}`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data || "Failed to fetch type");
        }
    }

    public static async add(groupID: string, item: any): Promise<any> {
        try {
            const response = await api.post(`ps_groups/${groupID}/ps_types`, item);
            if (response.data.ID) {
                // Assuming cache is a global object with remove method
                cache.remove(`collection${groupID}`);
                return response.data;
            } else {
                throw new Error("Failed to add type");
            }
        } catch (error) {
            throw new Error(error.response?.data || "Failed to add type");
        }
    }

    public static async edit(groupID: string, item: any): Promise<any> {
        const def = { resolve: null as ((value: any) => void), reject: null as ((reason?: any) => void) };
        
        try {
            // Assuming Restangular is no longer used and replaced with api.post
            const response = await api.put(`ps_groups/${groupID}/ps_types`, item);
            if (response.data.ID) {
                cache.remove(`collection${groupID}`);
                def.resolve(response.data);
            } else {
                def.reject(new Error("Failed to edit type"));
            }
        } catch (error) {
            def.reject(error.response?.data || new Error("Failed to edit type"));
        }

        return new Promise((resolve, reject) => {
            def.resolve = resolve;
            def.reject = reject;
        });
    }
}

export default TypeService;