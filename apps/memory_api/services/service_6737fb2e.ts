import { useState } from 'react';
import api from '@/lib/api';

interface Calculation {
  priceTotal?: string | number;
  volume?: number;
}

export default function PricingComponent() {
  const [calculation, setCalculation] = useState<Calculation>({});
  const [netPerPcs, setNetPerPcs] = useState<string>('0.00');

  // Example usage of the calculation logic within an async function
  const updatePriceAndVolume = async () => {
    try {
      const response = await api.get('/your-endpoint');
      const data: Calculation = response.data;

      let tmpPriceTotal;
      if (data.priceTotal !== undefined) {
        if (typeof(data.priceTotal) === 'string') {
          tmpPriceTotal = data.priceTotal.replace(',', '.');
        } else {
          tmpPriceTotal = data.priceTotal.toString();
        }

        const price = parseFloat(tmpPriceTotal);
        
        if (data.volume !== undefined) {
          const netPerPcsValue = price / data.volume;
          setNetPerPcs(netPerPcsValue.toFixed(2).replace('.', ','));
        }
      }
    } catch (error) {
      console.error('Error fetching calculation:', error);
    }
  };

  return (
    <div>
      {/* Render your component UI */}
      <button onClick={updatePriceAndVolume}>Update Price and Volume</button>
      {netPerPcs}
    </div>
  );
}