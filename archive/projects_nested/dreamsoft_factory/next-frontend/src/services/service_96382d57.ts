import React, { useEffect } from 'react';
import api from '@/lib/api';

interface Props {
  product: any;
  format: any;
}

const ProductFormatChecker: React.FC<Props> = ({ product, format }) => {
  const [relatedFormats, setRelatedFormats] = React.useState([]);

  useEffect(() => {
    if (!format.relatedFormats) return;

    async function fetchRelatedFormats() {
      try {
        // Assuming the API call requires some ID or other data from 'product' and 'format'
        const response = await api.get('someEndpoint', { params: { id: product.id, formatId: format.formatID } });
        setRelatedFormats(response.data);
      } catch (error) {
        console.error(error.response?.data || error);
        // Assuming Notification is a custom hook or utility function
        Notification.error('Error');
      }
    }

    fetchRelatedFormats();
  }, [product.id, format.formatID]);

  const checkEmptyChoice = (complexProduct: any, attributeID: string) => {
    // Implementation of the original logic for checking empty choice
    if (!complexProduct.attributes[attributeID]) {
      console.warn('Attribute is not set');
      return false;
    }
    return true;
  };

  return (
    <div>
      {/* Render your related formats or other components based on 'relatedFormats' state */}
      {JSON.stringify(relatedFormats)}
    </div>
  );
};

export default ProductFormatChecker;