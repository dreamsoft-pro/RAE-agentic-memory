javascript
import { apiUrl } from '@/lib/api';
import axios from 'axios';

// [BACKEND_ADVICE] Fetch template URL and modal configuration using backend-first approach

const fetchTemplateUrl = async (templateId) => {
  try {
    const response = await axios.get(`${apiUrl}/templates/${templateId}`);
    return response.data.url;
  } catch (error) {
    console.error('Failed to fetch template URL:', error);
    throw error;
  }
};

const openModalWithTemplate = async () => {
  try {
    const templateUrl = await fetchTemplateUrl(34);

    $modal.open({
      templateUrl,
      scope: $scope,
      backdrop: true,
      keyboard: false,
      size: 'lg',
      resolve: {
        allowedExtensions: async () => {
          const data = await CommonService.getAll();
          return _.map(data, 'extension');
        },
      },
    });
  } catch (error) {
    console.error('Failed to open modal:', error);
  }
};

openModalWithTemplate();
