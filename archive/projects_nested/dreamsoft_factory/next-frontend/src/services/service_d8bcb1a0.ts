import { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

class CalculationController {
    async getNetPricePerPcs(req: NextApiRequest, res: NextApiResponse) {
        const calculation = req.query.calculation;
        
        if (calculation.deliveryPrice) {
            let price = parseFloat(calculation.priceTotalBrutto);
            
            if (calculation.deliveryPrice) {
                price += parseFloat(calculation.deliveryPrice);
            }

            const netPerPcs = (price / parseFloat(calculation.volume)).toFixed(2).replace('.', ',');
            res.status(200).json({ netPerPcs, totalNet: price.toFixed(2).replace('.', ',') });
        } else {
            res.status(400).json('');
        }
    }

    async getGrossPricePerPcs(req: NextApiRequest, res: NextApiResponse) {
        const calculation = req.query.calculation;
        
        if (calculation && calculation.priceTotalBrutto) {
            let price = parseFloat(calculation.priceTotalBrutto);
            
            if (calculation.deliveryGrossPrice) {
                price += parseFloat(calculation.deliveryGrossPrice);
            }

            const grossPerPcs = (price / parseFloat(calculation.volume)).toFixed(2).replace('.', ',');
            res.status(200).json({ grossPerPcs, totalGross: price.toFixed(2).replace('.', ',') });
        } else {
            res.status(400).json('');
        }
    }
}

export default new CalculationController();