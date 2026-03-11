import api from "@/lib/api";

class OngoingService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async getOperatorsWithSkills(taskID: number): Promise<any> {
        try {
            const response = await api.get([this.resource, 'operatorsWithSkills', taskID].join("/"));
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async getAllOperators(): Promise<any> {
        try {
            const response = await api.get([this.resource, 'operators'].join("/"));
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}