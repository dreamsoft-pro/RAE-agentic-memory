/**
 * Service: group
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import './group.css'; // Assuming you have a corresponding CSS file for styling

const GroupComponent: React.FC = () => {
    return (
        <div>
            <style jsx>{`
                .stickyStyle1 {
                    position: sticky;
                    top: 60px;
                }

                .LeftMenuProducts {
                    list-style: none;
                }

                .LeftMenuProducts > li {
                    width: 100%;
                    padding-left: 15px;
                    font-size: 14px !important;
                }

                .LeftMenuProducts > li > a {
                    padding-top: 10px !important;
                    padding-bottom: 10px !important;
                }

                .LeftMenuProductsItems {
                    list-style: none;
                }

                .LeftMenuProductsItems > li {
                    width: 100%;
                    padding-left: 15px;
                    font-size: 12px !important;
                }

                .LeftMenuProductsItems > li > a {
                    padding-top: 5px !important;
                    padding-bottom: 5px !important;
                }

                .panelRightOrderMax {
                    overflow: hidden;
                }

                @media (max-width: 932px) {
                    .stickyStyle1 {
                        position: relative;
                        top: 0;
                    }
                    .rowSticky1 {
                        height: auto;
                    }
                    .owfh {
                        overflow: hidden;
                    }
                }
            `}</style>
        </div>
    );
};

export default GroupComponent;