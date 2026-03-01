import api from "@/lib/api";

class UserService {
    static async editUserOptions(userID: string, data: any): Promise<any> {
        try {
            const response = await api.patch(`${resource}/${userID}/userOptions`, data);
            if (response.data.response) {
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    static async getRoles(user: any): Promise<any> {
        try {
            const def = { resolve: null, reject: null };
            
            api.get(`${user}/roles`)
                .then((response) => {
                    if (response.data.success) {
                        def.resolve(response.data);
                    } else {
                        throw new Error('Failed to get roles');
                    }
                })
                .catch((error) => {
                    console.error(error);
                    def.reject(error);
                });

            // Since the API call is asynchronous, we need to return a promise that resolves once the API call completes
            return new Promise((resolve, reject) => {
                def.resolve = resolve;
                def.reject = reject;
            });
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
}