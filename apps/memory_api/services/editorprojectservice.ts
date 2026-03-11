javascript
import axios from '@/lib/api';

const getProjectsData = (url, header, projects) => {
    const config = {
        url: `${url}/getProjectsData`,
        method: 'POST',
        headers: header,
        data: { projects },
        crossDomain: true,
        withCredentials: true
    };

    // [BACKEND_ADVICE] Handle promise resolution and rejection
    return axios.request(config).then(response => response.data)
                             .catch(error => Promise.reject(error.response.status));
};

export default getProjectsData;
