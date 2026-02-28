javascript
import { backendApiCall } from '@/lib/api';

const TemplateRootService = {};

const resource = 'templates';

TemplateRootService.getTemplateUrl = function (templateID) {
    return backendApiCall('GET', [resource, 'getUrl', templateID].join('/'));
};

export default TemplateRootService;
