javascript
'use strict';

import { API_URL } from '@/lib/api';
import { BACKEND_ADVICE } from '@/utils/constants'; // Assuming constants file for backend advice

const UploadService = {};

BACKEND_ADVICE; // Marking this section as heavy logic might be handled by backend

function getGraphicsResource() {
    return 'graphicsUpload';
}

function getTextAngularUploadResource() {
    return 'taUploadIcons';
}

UploadService.getLogoUploadUrl = function () {
    return `${API_URL}/${getGraphicsResource()}`;
};

UploadService.getTAUploadUrl = function () {
    return `${API_URL}/${getTextAngularUploadResource()}`;
};

UploadService.getModelIconsUploadUrl = function () {
    return `${API_URL}/${getGraphicsResource()}/modelIcon`;
};
