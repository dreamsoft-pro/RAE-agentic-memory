import api from '@/lib/api';

export class PsCalculateService {
    private groupID: string;
    private typeID: string;
    private resource: string;

    constructor(groupID: string, typeID: string) {
        this.groupID = groupID;
        this.typeID = typeID;
        this.resource = `ps_groups/${groupID}/ps_types/${typeID}/ps_calculate`;
    }

    public async request(method: 'GET' | 'POST', endpoint?: string, data?: any): Promise<any> {
        const url = `${api.API_URL}${this.resource}${endpoint ? '/' + endpoint : ''}`;
        
        try {
            let response;
            
            if (method === 'GET') {
                response = await fetch(url);
            } else if (method === 'POST') {
                response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
            }

            const dataResponse = await response.json();
            
            return dataResponse;
        } catch (error) {
            throw new Error(`Failed to make ${method} request to ${url}: ${error}`);
        }
    }
}