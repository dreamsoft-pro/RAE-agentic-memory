/**
 * Service: wcga
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const WcgaComponent = () => {
    const changeContrast = () => {
        console.log('Change contrast clicked');
    };

    const toggleFontSize = () => {
        console.log('Toggle font size clicked');
    };

    return (
        <ul className="nav navbar-nav">
            <li>
                <a onClick={changeContrast} title="contrast">
                    <i className="fa fa-adjust"></i>
                </a>
            </li>
            <li>
                <a onClick={toggleFontSize} title="font_size">
                    <i className="fa fa-font"></i>
                </a>
            </li>
        </ul>
    );
};

export default WcgaComponent;