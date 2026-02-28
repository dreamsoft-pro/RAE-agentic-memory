import api from '@/lib/api';

export default class TemplateVariablesFetcher {
    private templateName: string;
    private groupID?: number;
    private typeID?: number;
    private categoryID?: number;
    private all?: boolean;

    constructor(templateName: string, groupID?: number, typeID?: number, categoryID?: number, all?: boolean) {
        this.templateName = templateName;
        this.groupID = groupID;
        this.typeID = typeID;
        this.categoryID = categoryID;
        this.all = all;
    }

    public async fetchVariables(): Promise<any> {
        const resource: string = 'templateVariables/getVariables';
        let params: string[] = ['templateName=' + this.templateName];

        if (this.groupID !== undefined) {
            params.push('groupID=' + this.groupID);
        }
        if (this.typeID !== undefined) {
            params.push('typeID=' + this.typeID);
        }
        if (this.categoryID !== undefined) {
            params.push('categoryID=' + this.categoryID);
        }
        if (this.all !== undefined) {
            params.push('all=' + this.all);
        }

        let url: string = `${api.API_URL}${resource}`;
        if (params.length > 0) {
            url += '?' + params.join('&');
        }

        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}