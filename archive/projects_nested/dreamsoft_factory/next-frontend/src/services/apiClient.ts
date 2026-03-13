/**
 * apiClient.ts
 * Standardized API client for Dreamsoft Pro 2.0.
 * Connects to the High-Power Backend on Node 1 (Lumina).
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://100.68.166.117:9595';

export const apiClient = {
  request: async (method: string, endpoint: string, data?: any) => {
    // Ensure endpoint starts with /
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest', // For legacy PHP compatibility
        },
        body: data ? JSON.stringify(data) : undefined,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP Error ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`[API ${method}] Error at ${url}:`, error);
      throw error;
    }
  },

  get: (url: string) => apiClient.request('GET', url),
  post: (url: string, data: any) => apiClient.request('POST', url, data),
  put: (url: string, data: any) => apiClient.request('PUT', url, data),
  delete: (url: string) => apiClient.request('DELETE', url),
};
