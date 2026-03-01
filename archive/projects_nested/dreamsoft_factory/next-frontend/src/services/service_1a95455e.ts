import api from '@/lib/api';
import { DpCategoryService, SettingService, PaymentService } from '@digitalprint/services'; // Assuming these services are imported like this
import _ from 'lodash';

export default class MainWidgetService {
    private $filter: any; // Replace with actual types as needed
    private $config: any;
    
    constructor(private dpCategoryService: DpCategoryService, private paymentService: PaymentService) {}

    public async getMegaMenu(): Promise<any[]> {
        try {
            const categories = await this.dpCategoryService.getCategoryTree();
            if (_.size(categories) > 0) {
                return categories;
            } else {
                throw new Error('No categories found');
            }
        } catch (error) {
            console.error(error);
            throw error; // or handle the rejection as needed
        }
    }

    public async getCreditLimit(): Promise<any> {
        try {
            const data = await this.paymentService.getCreditLimit();
            return data;
        } catch (error) {
            console.error('Failed to fetch credit limit:', error);
            throw error; // or handle the rejection as needed
        }
    }

    public async getSkinName(): Promise<string> { // Example method, actual implementation needed
        try {
            const skinName = await this.someMethodThatGetsSkinName(); // Replace with actual logic
            return skinName;
        } catch (error) {
            console.error('Failed to fetch skin name:', error);
            throw error; // or handle the rejection as needed
        }
    }

    private someMethodThatGetsSkinName(): Promise<string> { // Dummy method, replace with actual implementation
        return api.get('/some-endpoint'); // Example API call
    }
}