import api from '@/lib/api';

class UserService {
    private static async userDataChange(data: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${resource}/changeUserData`, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Failed to change user data');
            }
        } catch (error) {
            throw error;
        }
    }

    private static async changeMail(data: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${resource}/changeEmail`, data);
            return response.data;
        } catch (error) {
            throw new Error('Failed to change email');
        }
    }

    // Assuming resource is a global variable or passed as an argument
    private static getResource(): string {
        if (!this.resource) {
            throw new Error("Resource must be defined");
        }
        return this.resource;
    }

    public static resource: string = '';  // Initialize with the appropriate value

    constructor() {
        if (!UserService.resource) {
            throw new Error('Resource must be set before using UserService');
        }
    }
}

// Usage example:
(async () => {
    try {
        const userDataResponse = await UserService.userDataChange({ /* your data */ });
        console.log(userDataResponse);
        
        const changeMailResponse = await UserService.changeMail({ /* your data */ });
        console.log(changeMailResponse);
    } catch (error) {
        console.error(error.message);
    }
})();