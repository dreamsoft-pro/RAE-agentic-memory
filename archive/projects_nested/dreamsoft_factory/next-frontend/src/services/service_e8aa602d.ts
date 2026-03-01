import api from "@/lib/api";

class CalculateService {
    private readonly url: string;

    constructor(url: string) {
        this.url = url; // Ensure the URL is defined before use
    }

    private async request<T>(method: string, resource: string, data?: any): Promise<T> {
        const response = await api[method.toLowerCase()]({
            url: `${this.url}${resource}`,
            data,
        });

        if (response.data.response) {
            return response.data;
        } else {
            throw new Error(JSON.stringify(response.data));
        }
    }

    public async calculate(item: any): Promise<any> {
        return this.request('POST', '', item);
    }

    public async getVolumes(item: any): Promise<any> {
        return this.request('PATCH', '', item);
    }

    public async saveCalculation(preparedProduct: any): Promise<any> {
        return this.request('POST', 'saveCalculation', preparedProduct);
    }
}

export default CalculateService;