import api from '@/lib/api';
import { useState, useEffect } from 'react';

interface ComplexProduct {
    selectedProduct: {
        data: {
            currentFormat: {
                maxHeight: number;
                maxWidth: number;
                slope: number;
                customHeight: number;
            };
        };
    };
}

const MyComponent = (props: Partial<ComplexProduct>) => {
    const [complexProduct, setComplexProduct] = useState<ComplexProduct>({
        selectedProduct: { data: { currentFormat: { maxHeight: 0, maxWidth: 0, slope: 0, customHeight: 0 } } }
    });

    useEffect(() => {
        if (props.selectedProduct) {
            const updatedProduct = props;
            setComplexProduct(updatedProduct);
        }

        // Perform other initialization logic or API calls here
    }, [props]);

    const handleFormatChange = () => {
        let maxHeight: number, maxWidth: number;

        maxHeight = complexProduct.selectedProduct.data.currentFormat.maxHeight - complexProduct.selectedProduct.data.currentFormat.slope * 2;
        maxWidth = complexProduct.selectedProduct.data.currentFormat.maxWidth - complexProduct.selectedProduct.data.currentFormat.slope * 2;

        if (complexProduct.selectedProduct.data.currentFormat.customHeight > maxHeight) {
            Notification.info($filter('translate')('value_greater_than_maximum') + ' ' + maxHeight);
            complexProduct.selectedProduct.data.currentFormat.customHeight = maxHeight;
            setComplexProduct({ ...complexProduct });
        }
    };

    // Simulating a function that might trigger the format change
    useEffect(() => {
        handleFormatChange();
    }, [complexProduct]);

    return (
        <div>
            {/* Your JSX here */}
        </div>
    );
};

export default MyComponent;