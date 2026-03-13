import api from '@/lib/api';
import { useState, useEffect } from 'react';

interface PsConfigPaperPriceOptions {
  attrID: number;
  optID: number;
}

class PsPaperPriceService {
  private cache: any; // Assuming a caching mechanism similar to Angular's $cacheFactory
  private resource?: string;

  constructor(attrID: number = 0, optID: number = 0) {
    this.cache = {}; // Placeholder for actual caching logic
    this.setResource(attrID, optID);
  }

  public getResource(): string | undefined {
    return this.resource;
  }

  private setResource(attrID: number, optID: number): void {
    if (attrID === 0 && optID === 0) {
      throw new Error('Both attrID and optID must be non-zero integers.');
    }
    this.resource = `ps_attributes/${attrID}/ps_options/${optID}/paperPrice`;
  }

  public async getAll(force?: boolean): Promise<any> {
    if (!this.resource) {
      return;
    }

    // Placeholder for actual cache logic
    const cachedData = this.cache[this.resource];
    let promise: Promise<any>;

    if (cachedData && !force) {
      promise = Promise.resolve(cachedData);
    } else {
      promise = api.get(this.resource).then(response => response.data).catch(error => {
        throw new Error(`Failed to fetch data for resource ${this.resource}: ${error.message}`);
      });
    }

    return promise;
  }
}

export default PsPaperPriceService;