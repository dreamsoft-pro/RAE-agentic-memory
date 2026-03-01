/**
 * Service: 404
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import './404.css'; // Assuming you have a corresponding CSS file for styling

const NotFoundPage: React.FC = () => {
    return (
        <div className="container">
            <h1>Not Found</h1>
            <p>Sorry, but the page you were trying to view does not exist.</p>
            <a href="/{{lang}}">Go to home page</a>
        </div>
    );
};

export default NotFoundPage;