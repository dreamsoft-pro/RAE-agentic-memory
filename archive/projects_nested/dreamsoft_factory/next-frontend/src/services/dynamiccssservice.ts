javascript
import { BackendApi } from '@/lib/api';
import '@angular/core';

const DynamicCssService = {};

DynamicCssService.loadDomainCSS = function(domainID, companyID) {
    const staticUrl = $config.STATIC_URL || 'http://localtest.me/static/';
    const cssLink = document.createElement('link');

    cssLink.rel = 'stylesheet';
    cssLink.type = 'text/css';
    cssLink.href = `${staticUrl}${companyID}/styles/${domainID}/main.css`;

    // Remove any existing domain-specific CSS
    const existingLink = document.querySelector('#dynamic-css');
    if (existingLink) {
        existingLink.parentNode.removeChild(existingLink);
    }

    // Set an ID for easier management
    cssLink.id = 'dynamic-css';

    document.head.appendChild(cssLink);
};

export { DynamicCssService };
