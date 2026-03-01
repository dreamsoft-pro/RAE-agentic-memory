import { useEffect, useState } from 'react';
import api from '@/lib/api';

interface LabelImposition {
    ID?: number;
    labelRotation: string | number;
    rotationAngle: string | number;
}

const PrintshopLabelImpositionCtrl = () => {
    const [labelImposition, setLabelImposition] = useState<LabelImposition>({ labelRotation: 0, rotationAngle: 0 });

    useEffect(() => {
        async function fetchLabelImposition() {
            try {
                const currentTypeID = Number(window.location.search.split('typeID=')[1].split('&')[0]); // Assuming typeID is passed as a query parameter
                if (!isNaN(currentTypeID)) {
                    const response = await api.get(`/api/label-imposition/${currentTypeID}`);
                    setLabelImposition(response.data);
                    fixTypes();
                }
            } catch (error) {
                console.error('Failed to fetch label imposition data', error);
            }
        }

        fetchLabelImposition();
    }, []);

    const fixTypes = () => {
        if (typeof labelImposition.labelRotation === 'number') {
            setLabelImposition((prev) => ({ ...prev, labelRotation: prev.labelRotation.toString() }));
        }
        if (typeof labelImposition.rotationAngle === 'number') {
            setLabelImposition((prev) => ({ ...prev, rotationAngle: prev.rotationAngle.toString() }));
        }
    };

    return (
        <div>
            {/* Your JSX code here */}
        </div>
    );
};

export default PrintshopLabelImpositionCtrl;