import api from '@/lib/api';

class OperatorService {

    static async updateOperatorSkills(operator: { ID: string }, resource: string, skills: any): Promise<any> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/${operator.ID}/operatorSkills`;
        
        try {
            const response = await api.patch(url, skills);
            
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response data indicates failure');
            }
        } catch (error: any) {
            console.error('Error updating operator skills', error);
            throw error; // Rethrow the error to ensure it's handled upstream
        }
    }

    static logs(operator: { ID: string }, config: any): any {
        const res = [resource, operator.ID, 'operatorLogs'].join("/");
        
        if (config) {
            config.count = `${res}/count`;
        }

        return new ApiCollection(res, config);
    }

    static getOperator(operatorID: string): Promise<any> {
        return api.get(`${process.env.NEXT_PUBLIC_API_URL}/${resource}/${operatorID}`).then(response => response.data).catch(error => {
            console.error('Error fetching operator', error);
            throw error;
        });
    }
}

// Assuming ApiCollection is defined elsewhere in your project
class ApiCollection {
    constructor(private url: string, private config: any) {}

    // Further implementation of the class would go here...
}