javascript
import { callApi } from '@/lib/api';

function calculateAndPrintOffer(data) {
    return callApi({
        method: 'PATCH',
        url: `${process.env.API_URL}/calculate/printOffer`,
        data,
    }).then(response => response.data)
      .catch(error => Promise.reject(error));
}

// [BACKEND_ADVICE] Heavy logic should be handled in the backend as per LEAN DESIGN principle.
export default calculateAndPrintOffer;
