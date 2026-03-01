import { useEffect, useState } from 'react';
import axios from '@/lib/api';

export default class ContentService {
  private routeID: string;
  private resource: string;
  private cacheKey: string = 'mainContents';
  private cachedData?: any;

  constructor(routeID: string) {
    this.routeID = routeID;
    this.resource = ['routes', routeID, 'mainContents'].join('/');
  }

  public async getAll(force = false): Promise<any> {
    if (!force && this.cachedData !== undefined) {
      return this.cachedData;
    }

    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}${this.resource}`);
      this.cachedData = response.data; // Cache the data for future requests
      return response.data;
    } catch (error: any) {
      throw new Error(error.response ? error.response.statusText : 'Network Error');
    }
  }

  public async getAllCache(force = false): Promise<any> {
    if (!force && this.cachedData !== undefined) {
      return this.cachedData; // Return cached data if not forced
    } else if (force || !this.cachedData) {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}${this.resource}`);
        this.cachedData = response.data;
        return response.data;
      } catch (error: any) {
        throw new Error(error.response ? error.response.statusText : 'Network Error');
      }
    }

    // This part should be adjusted based on the rest of your logic
    // If you have a way to keep track of pending requests, add it here.
  }
}