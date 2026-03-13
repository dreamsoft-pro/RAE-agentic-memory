import api from '@/lib/api';
import { useEffect, useState } from 'react';

export default function ProductComponent() {
  const [complexProduct, setComplexProduct] = useState({
    selectedProduct: {
      data: {
        currentFormat: {
          customHeight: '',
          customWidth: '',
          minHeight: 0,
          minWidth: 0,
          slope: 0
        }
      }
    },
    stopSelect: undefined
  });

  useEffect(() => {
    // Update custom height and width if they are not numbers
    complexProduct.selectedProduct.data.currentFormat.customHeight = Number(complexProduct.selectedProduct.data.currentFormat.customHeight);
    complexProduct.selectedProduct.data.currentFormat.customWidth = Number(complexProduct.selectedProduct.data.currentFormat.customWidth);

    const cancelTimeout = () => {
      if (complexProduct.stopSelect) {
        clearTimeout(complexProduct.stopSelect as number);
        setComplexProduct((prev) => ({ ...prev, stopSelect: undefined }));
      }
    };

    // Simulate the $timeout functionality
    let timeoutId;
    const scheduleFunctionAfterDelay = async () => {
      if (complexProduct.selectedProduct.data.currentFormat.minHeight && complexProduct.selectedProduct.data.currentFormat.slope &&
          complexProduct.selectedProduct.data.currentFormat.minWidth) {
        try {
          await someAsyncOperation();
          // Function to run after the timeout
          console.log(`Min Height: ${complexProduct.selectedProduct.data.currentFormat.minHeight}`);
          console.log(`Min Width: ${complexProduct.selectedProduct.data.currentFormat.minWidth}`);

          const minHeight = complexProduct.selectedProduct.data.currentFormat.minHeight - complexProduct.selectedProduct.data.currentFormat.slope * 2;
          const minWidth = complexProduct.selectedProduct.data.currentFormat.minWidth - complexProduct.selectedProduct.data.currentFormat.slope * 2;

          console.log(`Min Height Adjusted: ${minHeight}`);
          console.log(`Min Width Adjusted: ${minWidth}`);

        } catch (error) {
          console.error('Error during async operation', error);
        }
      }

      timeoutId = setTimeout(scheduleFunctionAfterDelay, 1000); // Example delay
    };

    scheduleFunctionAfterDelay();
    
    return () => clearTimeout(timeoutId);

  }, [complexProduct]);

  const someAsyncOperation = async () => {
    try {
      const response = await api.get('/some-endpoint');
      console.log('Response:', response.data);
    } catch (error) {
      console.error('Error fetching data', error);
    }
  };
}