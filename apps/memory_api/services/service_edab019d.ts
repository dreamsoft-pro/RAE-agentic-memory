import api from '@/lib/api';

class PsConfigOption {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    getResource(): string {
        return this.resource;
    }

    deleteSideRelation(optID: number, controllerID: number, id: number): Promise<any> {
        const url = `${process.env.API_URL}/${[this.getResource(), optID, 'efficiency', controllerID, 'sideRelations', id].join('/')}`;

        return api.delete(url)
            .then(response => response.data) // Assuming the API returns data in the `data` field
            .catch(errorResponse => Promise.reject(errorResponse));
    }

    static getControllerService(type: number): PsConfigOption {
        switch (type) {
            case 1:
                return new PsPricelistService();
            case 2:
                return new PsPrintTypeService();
            case 3:
                return new PsWorkspaceService();
            default:
                throw new Error('Unknown service type');
        }
    }

    getRelativeOptionsFilter(optID: number): Promise<any> {
        const url = `${process.env.API_URL}/${[this.getResource(), optID, 'relativeOptionsFilter'].join('/')}`;

        return api.get(url)
            .then(response => response.data) // Assuming the API returns data in the `data` field
            .catch(errorResponse => Promise.reject(errorResponse));
    }
}