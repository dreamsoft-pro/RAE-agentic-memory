import api from '@/lib/api';
import { useRouter } from 'next/router'; // Assuming you need router for some context or similar import

class ProductDetails extends React.Component {
    complexProduct: any;
    attributeID: number;

    constructor(props) {
        super(props);
        this.complexProduct = props.complexProduct; // Example of how to initialize complexProduct
        this.attributeID = parseInt(this.props.routeParams.id); // Example initialization, adjust as necessary
    }

    async getEmptyChoice(): Promise<boolean | string> {
        const attrIdx = _.findIndex(this.complexProduct.selectedProduct.data.attributes, { attrID: this.attributeID });

        if (attrIdx > -1) {
            const attribute = this.complexProduct.selectedProduct.data.attributes[attrIdx];
            const optionID = this.complexProduct.selectedProduct.data.selectedOptions[attribute.attrID];

            const optIdx = _.findIndex(attribute.filteredOptions, { ID: parseInt(optionID) });
            if (optIdx > -1) {
                const option = attribute.filteredOptions[optIdx];
                return option.emptyChoice;
            }
        }

        return false;
    }
}