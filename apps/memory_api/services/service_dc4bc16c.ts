import api from '@/lib/api';

class LabelImpositionService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async generate(labelImpositionID: string | number, dpProductID: string | number, calcProductID: string | number, calcProductFileID: string | number, copyToSpecialFolders: boolean): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/generate/${labelImpositionID}/${dpProductID}/${calcProductID}/${calcProductFileID}/${copyToSpecialFolders}`);
            return response.data;
        } catch (error) {
            throw error.response || error;
        }
    }
}

export default LabelImpositionService;