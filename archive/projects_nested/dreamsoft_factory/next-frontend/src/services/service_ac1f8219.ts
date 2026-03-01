import api from "@/lib/api";

class PsConfigOption {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async addEfficiencySideRelation(optID: string, controllerID: string, data: any): Promise<any> {
        try {
            const response = await api.post([this.getResource(), optID, 'efficiency', controllerID, 'sideRelations'].join("/"), data);
            return response.data;
        } catch (error) {
            throw error.response ? error : new Error("Failed to add efficiency side relation");
        }
    }

    async deleteEfficiencySideRelation(optID: string, controllerID: string, id: string): Promise<void> {
        try {
            await api.delete([this.getResource(), optID, 'efficiency', controllerID, 'sideRelations', id].join("/"));
        } catch (error) {
            throw error.response ? error : new Error("Failed to delete efficiency side relation");
        }
    }

    private getResource(): string {
        return this.resource;
    }
}