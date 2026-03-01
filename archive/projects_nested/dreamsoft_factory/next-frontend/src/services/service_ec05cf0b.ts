import api from "@/lib/api";

class DpStatusService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async sort(sortData: any): Promise<any> {
        const url = `${process.env.API_URL}/${this.resource}/sort`;

        try {
            const response = await api.patch(url, sortData);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error("Response error");
            }
        } catch (error: any) {
            console.error(error);
            throw error;
        }
    }
}

export default DpStatusService;