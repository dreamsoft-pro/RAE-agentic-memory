import api from '@/lib/api';
import _ from 'lodash';

export default class ProductSelector extends React.Component {
    selectOption(selectedProductData: any, attrID: string | number, item: any, noReload: boolean): void {
        const itemExist = this.checkItemExists(selectedProductData, attrID, item, noReload);
        
        if (itemExist) {
            // Assuming $scope.selectOption is a method that exists in the React component context
            this.$scopeSelectOption(selectedProductData, attrID, item, noReload);
        }
    }

    private async fetchExcludedOptions(productId: string | number): Promise<string[]> {
        const response = await api.get(`/api/products/${productId}/excluded-options`);
        return response.data;
    }

    private checkItemExists(selectedProductData: any, attrID: string | number, item: any, noReload: boolean): boolean {
        const productExcludedOptions = await this.fetchExcludedOptions(selectedProductData.ID);
        
        let tmp: any;

        item.options.forEach(option => {
            if (!_.includes(productExcludedOptions, option.ID)) {
                tmp = option;
                return false; // forEach loop should break here
            }
        });

        const defaultOption = _.find(item.options, { default: 1 });

        if (defaultOption && !_.includes(productExcludedOptions, defaultOption.ID)) {
            tmp = defaultOption;
        }

        this.$scopeSelectOption(selectedProductData, attrID, tmp, noReload);
        
        return true; // Assuming you want to signal that the item exists
    }

    private $scopeSelectOption(selectedProductData: any, attrID: string | number, item: any, noReload: boolean): void {
        console.log(`Selected product ID: ${selectedProductData.ID}, Attribute ID: ${attrID}, Item: `, item, `No reload: ${noReload}`);
        // Replace the console log with actual $scope.selectOption implementation
    }
}