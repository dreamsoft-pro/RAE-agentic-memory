import api from '@/lib/api';
import { useState } from 'react';

interface ProductItem {
    volume?: number;
}

const MyComponent = () => {
    const [productItem, setProductItem] = useState<ProductItem>({});
    const [rememberVolume, setRememberVolume] = useState<{ realisationTime: { volumes: Array<{ volume: number }> }} | null>(null);

    const handleApiCall = async () => {
        try {
            const response = await api.fetchData();
            // Handle success
        } catch (error) {
            Notification.error('Error occurred');
        }
    };

    const changeVolume = () => {
        if (!productItem.volume || !rememberVolume) return;

        const idx = rememberVolume.realisationTime.volumes.findIndex(volumeObj => volumeObj.volume === productItem.volume);

        // Handle index
    };

    return (
        <div>
            {/* Render component JSX */}
        </div>
    );
};

export default MyComponent;