import api from "@/lib/api";

export default class DiscountService {
    private resource: string = 'discounts'; // Define resource before use

    public async update(data: any): Promise<any> {
        try {
            const response = await api.put($config.API_URL + this.resource, data);
            if (response.response) {
                return response;
            } else {
                throw new Error(JSON.stringify(response));
            }
        } catch (error) {
            throw error; // Ensure errors are properly handled
        }
    }

    public async remove(id: string): Promise<any> {
        try {
            const url = `${$config.API_URL}/${this.resource}/${id}`;
            const response = await api.delete(url);
            if (response.response) {
                console.log(response.message);
                return response;
            } else {
                throw new Error(JSON.stringify(response));
            }
        } catch (error) {
            throw error; // Ensure errors are properly handled
        }
    }
}