/**
 * Service: TextWidgetService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

/**
 */
import { useState, useEffect } from 'react';
import DOMParser from 'domparser-shim'; // Assuming this is for parsing HTML to text

interface TextWidgetServiceProps {
    json: any;
}

const TextWidgetService = ({ json }: TextWidgetServiceProps) => {
    const [text, setText] = useState('');

    useEffect(() => {
        // Extend the service with JSON data
        Object.assign(this, json);
    }, [json]);

    const findWord = (html: string, lines: number): string | false => {
        const plainText = new DOMParser().parseFromString(html, "text/html").documentElement.textContent;
        if (!plainText) return false;
        const splitText = plainText.split(' ');

        let chars = 0;
        for (let i = 0; i < splitText.length; i++) {
            chars += splitText[i].length;
            if (chars >= lines) {
                return splitText[i];
            }
        }
        return false;
    };

    const findParagraph = (html: string, word: string): number | false => {
        const paragraphs = new DOMParser().parseFromString(html, "text/html").querySelectorAll('p');

        if (paragraphs.length === 1) return false;

        for (let i = 0; i < paragraphs.length; i++) {
            if (paragraphs[i].nextElementSibling) {
                const text = paragraphs[i].nextElementSibling.innerHTML.replace(/<[^>]*>/g, "");
                if (text.indexOf(word) !== -1) {
                    return i;
                }
            }
        }

        if (typeof word === 'string' && word.length > 0) {
            return 0;
        }
        return false;
    };

    const getLess = (html: string, paragraph: number): string | false => {
        const paragraphs = new DOMParser().parseFromString(html, "text/html").querySelectorAll('p');

        let template = '';
        for (let i = 0; i < paragraphs.length; i++) {
            template += paragraphs[i].innerHTML;
            if (paragraph === i) {
                return template;
            }
        }
        return false;
    };

    return (
        <div>
            {/* You can add more JSX elements here to interact with the service */}
        </div>
    );
};

export default TextWidgetService;