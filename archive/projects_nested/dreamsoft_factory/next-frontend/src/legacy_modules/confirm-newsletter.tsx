/**
 * Service: confirm-newsletter
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface ConfirmNewsletterProps {
    confirmation: {
        success?: string;
        error?: string;
    };
}

const ConfirmNewsletter: React.FC<ConfirmNewsletterProps> = ({ confirmation }) => {
    return (
        <div className="container" id="confirm-newsletter">
            <div className="row">
                <div className="col-xs-12">
                    {confirmation.success && (
                        <h1 className="page-header">
                            <i className="fa fa-check-circle"></i>
                            {confirmation.success}
                        </h1>
                    )}
                    {confirmation.error && (
                        <h1 className="page-header">
                            <i className="fa fa-close"></i>
                            {confirmation.error}
                        </h1>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ConfirmNewsletter;