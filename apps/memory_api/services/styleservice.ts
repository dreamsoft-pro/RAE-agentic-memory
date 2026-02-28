javascript
import { apiRequest } from '@/lib/api';

const StyleService = {};

StyleService.getMainFile = () => {
    return apiRequest('GET', 'mainCssFile');
};

StyleService.saveMainFile = (content) => {
    const data = {
        content: content
    };

    // [BACKEND_ADVICE] Consider handling potential backend logic here.
    return apiRequest('POST', 'saveMainCssFile', data);
};

export { StyleService };
