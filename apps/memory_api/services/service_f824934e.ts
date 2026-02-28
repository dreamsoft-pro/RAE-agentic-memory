import { useState, useEffect } from 'react';
import api from '@/lib/api';

interface Volume {
  volume: number;
  price?: number;
}

interface RealisationTime {
  ID: string;
  volumes: Volume[];
}

interface Calculation {
  rtID: string | null;
  volume: number | null;
  priceTotal: number | null;
}

const MyComponent = () => {
  const [realisationTimes, setRealisationTimes] = useState<RealisationTime[]>([]);
  const [calculation, setCalculation] = useState<Calculation>({
    rtID: null,
    volume: null,
    priceTotal: null
  });

  useEffect(() => {
    const fetchRealisationTimes = async () => {
      try {
        const response = await api.get('/realisation-times');
        setRealisationTimes(response.data);
      } catch (error) {
        console.error('Failed to fetch realisation times', error);
      }
    };

    fetchRealisationTimes();
  }, []);

  const handleVolumeChange = async (volume: Volume, idxRT: number) => {
    let idxV = -1;
    for (let i = 0; i < realisationTimes[idxRT].volumes.length; i++) {
      if (realisationTimes[idxRT].volumes[i].volume === volume.volume) {
        idxV = i;
        break;
      }
    }

    if (idxV !== -1) {
      setCalculation(prev => ({
        ...prev,
        rtID: realisationTimes[idxRT].ID,
        volume: realisationTimes[idxRT].volumes[idxV].volume,
        priceTotal: realisationTimes[idxRT].volumes[idxV].price
      }));
    }
  };

  return (
    <div>
      {/* Your component JSX */}
    </div>
  );
};

export default MyComponent;