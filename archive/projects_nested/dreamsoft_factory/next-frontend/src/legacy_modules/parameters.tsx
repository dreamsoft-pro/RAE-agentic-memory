/**
 * Service: parameters
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface RealizationTime {
    ID: number;
    names: { [key: string]: string };
    order: number;
}

interface Lang {
    code: string;
}

interface Product {
    langs: { [key: string]: { name: string } };
}

interface Props {
    realisationTimes: RealizationTime[];
    currentLang: Lang;
    type: { turnOnNumberOfSets: number };
    filterRealisationTime: (value: any) => boolean;
}

const ParametersForm: React.FC<Props> = ({ realisationTimes, currentLang, type, filterRealisationTime }) => {
    const [productItem, setProductItem] = React.useState({ realisationTime: '' });
    const [numberOfPatterns, setNumberOfPatterns] = React.useState(1);

    const handleRealizationTimeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setProductItem({ ...productItem, realisationTime: event.target.value });
    };

    const handleCustomAmountSpin = (direction: string) => {
        // Implement the logic to adjust the number of sets
    };

    return (
        <div>
            <div className="form-group">
                <label className="col-md-5 control-label">{'product' | translate}</label>
                <div className="col-md-7">
                    <select className="form-control" onChange={(e) => handleProductChange(e.target.value)}>
                        {complexProduct.products.map((product, index) => (
                            <option key={index} value={product.ID}>{product.langs[currentLang.code].name}</option>
                        ))}
                    </select>
                </div>
            </div>

            {type.turnOnNumberOfSets === 1 && (
                <div className="form-group">
                    <label className="col-md-5 control-label">{'number_of_patterns' | translate}</label>
                    <div className="col-md-7">
                        <div className="input-group spincontainer">
                            <div className="input-group-btn">
                                <button type="button" className="btn btn-default" onClick={() => handleCustomAmountSpin('dwn')}>
                                    <i className="fa fa-minus"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ParametersForm;