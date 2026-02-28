/**
 * httpBridge.ts
 * Legacy Compatibility Layer.
 * Proxies old AngularJS $http calls to the new Next.js apiClient.
 */

import { apiClient } from '../services/apiClient';

export const $http = {
  get: (url: string, config?: any) => apiClient.get(url),
  post: (url: string, data: any, config?: any) => apiClient.post(url, data),
  put: (url: string, data: any, config?: any) => apiClient.put(url, data),
  delete: (url: string, config?: any) => apiClient.delete(url),
  
  // AngularJS style call $http({method: '...', url: '...'})
  async (config: any) => {
    return apiClient.request(config.method || 'GET', config.url, config.data);
  }
};

// Also provide a helper for standard Dreamsoft defer/promise pattern
export const $q = {
  defer: () => {
    let resolve: any, reject: any;
    const promise = new Promise((res, rej) => {
      resolve = res;
      reject = rej;
    });
    return {
      promise,
      resolve: (val: any) => resolve(val),
      reject: (reason: any) => reject(rej)
    };
  },
  when: (val: any) => Promise.resolve(val),
  all: (promises: Promise<any>[]) => Promise.all(promises)
};
