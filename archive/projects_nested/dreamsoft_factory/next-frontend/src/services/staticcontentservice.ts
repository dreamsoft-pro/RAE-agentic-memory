javascript
'use strict';

import { BackendApi } from '@/lib/api';
import { BACKEND_ADVICE } from './constants'; // Assuming constants file contains backend advice

const StaticContentService = {
  getContent: function(key) {
    BACKEND_ADvice('Fetching static content for key: ' + key);
    return new Promise((resolve, reject) => {
      BackendApi.getStaticContentForKey(resource(), key)
        .then(response => resolve(response.data))
        .catch(error => {
          console.log(error);
          reject(error);
        });
    });
  }
};

function resource() {
  return ['dp_static_contents'];
}

export default StaticContentService;
