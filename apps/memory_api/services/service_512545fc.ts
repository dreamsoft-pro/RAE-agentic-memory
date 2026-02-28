import { useEffect, useState } from 'react';
import api from '@/lib/api';

interface Product {
  productID: string;
}

interface File {
  ID: number;
  name: string;
}

const useProductFiles = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [product, setProduct] = useState<Product | null>(null);

  useEffect(() => {
    (async () => {
      if (!product) return;

      try {
        const response = await api.getProductFiles(product.productID);
        setFiles(response.files);
      } catch (error) {
        console.error('Error fetching product files', error);
      }
    })();
  }, [product]);

  const acceptReport = async (file: File, scope: any) => {
    try {
      const response = await api.acceptReport(product.productID, file.ID);

      if (response.reportAccepted) {
        console.info(`report_accepted ${file.name}`);
      }

      if (response.productAccepted) {
        console.info('product_accepted');
      }

      scope.getNextPage(scope.pagingSettings.currentPage);
    } catch (error) {
      console.error('Error accepting report', error);
    }
  };

  return { files, acceptReport };
};

export default useProductFiles;