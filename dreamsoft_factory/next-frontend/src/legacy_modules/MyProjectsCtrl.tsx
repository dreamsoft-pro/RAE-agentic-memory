/**
 * Service: MyProjectsCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';

const MyProjectsCtrl: React.FC = () => {
    const [height, setHeight] = useState(0);
    const [width, setWidth] = useState(0);
    const [aspect, setAspect] = useState(0);

    useEffect(() => {
        const flipbookHolder = document.getElementById('flipbook');
        if (flipbookHolder) {
            let height = window.innerHeight * 0.8;
            let aspect = height / this.height;
            let width = (this.width * 2) * aspect;

            flipbookHolder.style.paddingTop = `${(height - window.innerHeight) / 2}px`;

            $(flipbookHolder).turn({
                height: height,
                width: width,
                autoCenter: true,
            });

            $('.remove-flipbook').on('click', function (e) {
                e.stopPropagation();
                $(this).parent().remove();
            });

            $('.nextPage-flipbook').on('click', function (e) {
                $("#flipbook").turn('next');
            });

            $('.prevPage-flipbook').on('click', function (e) {
                $("#flipbook").turn("previous");
            });

            $(document).keyup(function(e) {
                if (e.keyCode === 27) {
                    $("#flipbook").turn("destroy").remove();
                }
                e.stopPropagation();
            });
        }
    }, []);

    return <div id="flipbook"></div>;
};

export default MyProjectsCtrl;