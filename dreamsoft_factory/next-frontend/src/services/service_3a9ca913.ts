import api from '@/lib/api';

class CalculateService {
    private resource: string;

    constructor(groupID: number, typeID: number) {
        this.resource = `groups/${groupID}/types/${typeID}`;
    }

    public async getVolumes(preparedProduct: any): Promise<void> {
        try {
            const response = await api.get(`${this.resource}/volumes`);
            const data = response.data;

            if (data.technologies && data.technologies.length === 0) {
                // Assuming technologies is a state or property that needs to be set
                // In a React/Next.js context, you would typically use setState or some other reactive method.
                console.log('Setting technologies:', data.technologies);
            }

            const activeVolumes = data.volumes.filter((element: any) => element.active === true);

            // Assuming showVolumes is a function that needs to be called
            this.showVolumes(data);
        } catch (error) {
            console.error('Failed to fetch volumes:', error);
        }
    }

    private showVolumes(data: any): void {
        // Implement the logic for showing volumes here.
        // This could involve calling a method on a parent component or setting state/reactive values.
        console.log('Showing volumes:', data.volumes);
    }
}

// Usage
const preparedProduct = { groupID: 1, typeID: 2 };
const calculateService = new CalculateService(preparedProduct.groupID, preparedProduct.typeID);

calculateService.getVolumes(preparedProduct).then(() => {
    // Handle any necessary logic after the volumes have been fetched and processed.
}).catch((error) => {
    console.error('Error in getVolumes:', error);
});