import api from '@/lib/api';

class ViewService {
    private routeID: string;
    private viewID: string;

    constructor(routeID: string, viewID: string) {
        this.routeID = routeID;
        this.viewID = viewID;
    }

    getResource(): string {
        // Implement the logic to return the resource
        return 'someResource';  // Replace with actual implementation
    }

    async sort(sort: any): Promise<any> {
        const resource = this.getResource();
        const data = {
            orders: sort,
            routeID: this.routeID
        };

        try {
            const response = await api.patch(`${resource}/sort`, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error;
        }
    }

    async getAllVariables(): Promise<any> {
        const resource = this.getResource();

        try {
            const response = await api.get(`${resource}/variables?viewID=${this.viewID}`);
            console.log(response.data);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default ViewService;