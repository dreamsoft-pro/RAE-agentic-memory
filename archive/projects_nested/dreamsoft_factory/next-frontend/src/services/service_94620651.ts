import api from '@/lib/api';

class YourClass {
    private scope: Record<string, any> = {};

    async loadVariables(): Promise<void> {
        try {
            const resp = await api.get('/some-endpoint');
            for (const variable of resp.response) {
                this.scope[variable.name] = variable.value;
            }
        } catch (error) {
            console.log('load variables fail', error);
        }
    }

    getTemplateVariable(scope: Record<string, any>, collection: string, itemType: string, id: string | number, variableName: string, defaultValue: any): any {
        const selectedCollection = scope[collection];
        if (selectedCollection) {
            for (const item of selectedCollection) {
                if (item.name === variableName && item[itemType + 'ID'] === id) {
                    return item.value;
                }
            }
        }
        return defaultValue;
    }

    // You can also define async methods here if needed
}