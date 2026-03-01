import { useEffect } from 'react';
import axios from '@/lib/api'; // Assuming this module handles API calls and Axios setup

interface DynamicCssService {
    loadDynamicCSS(url: string): Promise<void>;
}

class DynamicCSS implements DynamicCssService {
    private document = (typeof window !== 'undefined' && window.document) || null;

    async loadDynamicCSS(url: string): Promise<void> {
        if (!this.document) return; // Ensure the script runs only in a browser environment

        const headElement = this.document.getElementsByTagName('head')[0];
        if (!headElement) return; // Ensure that there is a <head> element to append CSS link to

        const cssLink = this.document.createElement('link');
        cssLink.rel = 'stylesheet';
        cssLink.href = url;

        await new Promise<void>((resolve, reject) => {
            cssLink.onload = resolve;
            cssLink.onerror = () => reject(new Error(`Failed to load stylesheet at ${url}`));
            headElement.appendChild(cssLink);
        });
    }
}

export default DynamicCSS;