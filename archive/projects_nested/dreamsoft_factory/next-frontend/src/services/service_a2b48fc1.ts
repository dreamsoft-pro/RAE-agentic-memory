import api from '@/lib/api';

class DiscountService {

    private resource: string = 'discounts'; // Assuming 'resource' is supposed to be 'discounts'

    public getSelectedGroups(userID: number): Promise<any> {
        return api.get(`${this.resource}/selectedDiscountGroup/${userID}`).then((response) => response.data).catch(error => { throw error; });
    }

    public setSelectedGroups(userID: number, data: any): Promise<any> {
        return api.patch(`${this.resource}/selectedDiscountGroup/${userID}`, data).then((response) => response.data).catch(error => { throw error; });
    }
}