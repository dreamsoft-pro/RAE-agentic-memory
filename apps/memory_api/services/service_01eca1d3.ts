import React, { useEffect } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

interface ProductItem {
  volume?: string;
  realisationTime: string;
}

interface RealisationTimes {
  ID: string;
  volumes: Volume[];
  order: number;
}

interface Volume {
  volume: string;
  isActive: boolean;
}

function getActiveVolume(volumes: Volume[], defaultIndex = 0): Volume {
  return volumes.find(volume => volume.isActive) || volumes[defaultIndex];
}

function getActiveVolumeByVolume(volumes: Volume[], selectedVolume: string): Volume {
  return volumes.find(volume => volume.volume === selectedVolume && volume.isActive);
}

const ProductComponent: React.FC = () => {
  const router = useRouter();
  const { productItem } = router.query as { productItem: ProductItem };
  
  useEffect(() => {
    async function updateProductItem() {
      if (productItem?.volume === undefined) {
        const sortRealisationTimes = _.sortBy($scope.realisationTimes, 'order');
        let activeVolume = getActiveVolume(sortRealisationTimes[0].volumes);
        $scope.checkVolume(sortRealisationTimes[0], activeVolume);
        productItem.volume = activeVolume.volume;
      } else {
        const sortRealisationTimes = _.sortBy($scope.realisationTimes, 'order');
        const actualRealisationTime = _.find(sortRealisationTimes, { ID: productItem.realisationTime });
        let activeVolume = getActiveVolumeByVolume(actualRealisationTime.volumes, productItem.volume);
        $scope.checkVolume(actualRealisationTime, activeVolume);
        productItem.volume = activeVolume.volume;
      }
    }

    updateProductItem();
  }, [productItem]);

  return (
    <div>
      {/* Your component content */}
    </div>
  );
};

export default ProductComponent;