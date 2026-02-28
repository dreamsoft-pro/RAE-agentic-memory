/**
 * Service: logout-in-progress
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import './logout-in-progress.css'; // Assuming you have a corresponding CSS file for styling

const LogoutInProgress: React.FC = () => {
    return (
        <div className="container">
            <div className="row content-logout-in-progress">
                <div className="col-xs-12">
                    <h2>Trwa wylogowanie...</h2>
                </div>
            </div>
        </div>
    );
};

export default LogoutInProgress;