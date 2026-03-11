import api from "@/lib/api";

class DeviceService {

    private async addSideRelation(deviceId: string, data: any): Promise<any> {
        try {
            const response = await api.post(`${resource}/${deviceId}/deviceSideRelations`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    private async deleteSideRelation(deviceId: string, id: string): Promise<void> {
        try {
            const url = `${resource}/${deviceId}/deviceSideRelations/${id}`;
            await api.delete(url);
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

// Usage Example
const deviceService = new DeviceService();

async function testAddRelation() {
    try {
        const response = await deviceService.addSideRelation("123", { side: "left" });
        console.log(response);
    } catch (error) {
        console.error(error);
    }
}

async function testDeleteRelation() {
    try {
        await deviceService.deleteSideRelation("123", "456");
        console.log("Successfully deleted relation.");
    } catch (error) {
        console.error(error);
    }
}