javascript
'use strict';

import { createApiFunction } from '@/lib/api';
import $config from './config'; // Assuming config is stored in a separate file

const CommonService = {
  getAll: createApiFunction({
    method: 'GET',
    url: `${$config.API_URL}dp_ModelIconsExtensions`,
    successHandler: (data) => data,
    errorHandler: (error) => Promise.reject(error),
  }),
};

export default CommonService;
