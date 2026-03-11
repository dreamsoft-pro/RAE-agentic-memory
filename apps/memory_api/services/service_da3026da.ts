import api from "@/lib/api";

class ShiftService {
    private static async deleteResource(resource: string, id: number): Promise<void> {
        const url = `${process.env.API_URL}/${[resource, id].join("/")}`;
        try {
            await api.delete(url);
        } catch (error) {
            throw error;
        }
    }

    private static async sortResources(sort: any): Promise<void> {
        const resource = "shifts"; // Assuming 'shifts' as an example. You should replace this with the actual resource.
        const url = `${process.env.API_URL}/${[resource, 'sort'].join('/')}`;
        try {
            await api.patch(url, sort);
        } catch (error) {
            throw error;
        }
    }

    public static async delete(resource: string, id: number): Promise<void> {
        return ShiftService.deleteResource(resource, id);
    }

    public static async sort(sort: any): Promise<void> {
        return ShiftService.sortResources(sort);
    }
}