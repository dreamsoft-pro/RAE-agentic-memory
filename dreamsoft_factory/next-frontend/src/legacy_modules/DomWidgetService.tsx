/**
 * Service: DomWidgetService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import * as React from 'react';
import { useEffect, useState } from 'react';

interface DomWidgetServiceProps {
    mainSelector: string;
    positionSelector: string;
    widthSelector: string;
}

const DomWidgetService: React.FC<DomWidgetServiceProps> = ({ mainSelector, positionSelector, widthSelector }) => {
    const [wrapWidth, setWrapWidth] = useState(0);

    useEffect(() => {
        const configWrap = document.querySelector(widthSelector);
        if (configWrap) {
            setWrapWidth(configWrap.clientWidth);
        }
    }, [widthSelector]);

    useEffect(() => {
        const mainElement = document.querySelector(mainSelector);
        const panelHeading = document.querySelector(positionSelector);
        if (mainElement && panelHeading) {
            const position = getPosition(panelHeading);

            const handleScroll = () => {
                if (window.scrollY > position.y) {
                    mainElement.classList.add('fix-panel');
                    mainElement.style.width = `${wrapWidth}px`;
                } else {
                    mainElement.classList.remove('fix-panel');
                    mainElement.style.width = 'auto';
                }
            };

            const handleResize = () => {
                const newWrapWidth = configWrap?.clientWidth || 0;
                if (window.scrollY > position.y) {
                    mainElement.style.width = `${newWrapWidth}px`;
                }
            };

            window.addEventListener('scroll', handleScroll);
            window.addEventListener('resize', handleResize);

            return () => {
                window.removeEventListener('scroll', handleScroll);
                window.removeEventListener('resize', handleResize);
            };
        }
    }, [mainSelector, positionSelector, widthSelector, wrapWidth]);

    const getPosition = (element: Element): { x: number; y: number } => {
        let xPosition = 0;
        let yPosition = 0;

        while (element) {
            xPosition += element.offsetLeft - element.scrollLeft + element.clientLeft;
            yPosition += element.offsetTop - element.scrollTop + element.clientTop;
            element = element.offsetParent as Element;
        }

        return { x: xPosition, y: yPosition };
    };

    const hasClass = (element: Element, existClass: string): boolean => {
        return !!element.className.match(new RegExp('(\\s|^)' + existClass + '(\\s|$)'));
    };

    const addClass = (element: Element, newClass: string) => {
        if (!hasClass(element, newClass)) {
            element.className += " " + newClass;
        }
    };

    const removeClass = (element: Element, existClass: string) => {
        if (hasClass(element, existClass)) {
            const reg = new RegExp('(\\s|^)' + existClass + '(\\s|$)');
            element.className = element.className.replace(reg, ' ');
        }
    };

    return null;
};

export default DomWidgetService;