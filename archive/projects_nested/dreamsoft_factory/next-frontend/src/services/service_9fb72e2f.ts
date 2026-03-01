import api from '@/lib/api';
import { useEffect, useState } from 'react';

interface Product {
    attributes: Array<{ attrID: number; options: Array<{ volume?: number }> }>;
    selectedOptions?: {[key: number]: any};
}

const VolumeSelector = () => {
    const [volumes, setVolumes] = useState<number[]>([]);
    const [customVolume, setCustomVolume] = useState<{
        minVolume: number;
        newVolume: number | undefined;
    }>({ minVolume: 0, newVolume: undefined });

    useEffect(() => {
        if (volumes.length === 0) return;

        // Set the minimum volume based on the first volume available
        setCustomVolume(prevState => ({ ...prevState, minVolume: volumes[0] }));

        // If no custom volume is defined, set it to the minimum volume value
        if (!customVolume.newVolume) {
            setCustomVolume(prevState => ({ ...prevState, newVolume: volumes[0] }));
        }
    }, [volumes]);

    const selectDefaultOptions = (product: Product) => {
        product.attributes.forEach(item => {
            if (!product.selectedOptions?.[item.attrID]) {
                item.options.forEach(option => {
                    // Perform actions based on 'option' and 'item', as per your requirements.
                    // Note that this part is a placeholder for further logic to be added
                });
            }
        });
    };

    const fetchVolumes = async () => {
        try {
            const response = await api.get('/volumes');
            setVolumes(response.data);
        } catch (error) {
            console.error('Error fetching volumes', error);
        }
    };

    useEffect(() => {
        fetchVolumes();
    }, []);

    return (
        <div>
            {/* Render your component UI here */}
            <button onClick={() => selectDefaultOptions({ attributes: [], selectedOptions: {} })}>
                Select Default Options
            </button>
        </div>
    );
};

export default VolumeSelector;