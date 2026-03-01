import { useEffect } from 'react';
import axios, { AxiosPromise } from 'axios';

interface Domain {
  ID: string;
  // Add other properties as necessary
}

class DomainService {

  static async getDomain(id: string): Promise<Domain | null> {
    try {
      const domains = await this.getAll();
      const domain = domains.find(domain => domain.ID === id);
      if (domain) return domain;
      else throw new Error('Domain not found');
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  static async setDomain(id: string): Promise<void> {
    try {
      const domain = await this.getDomain(id);
      localStorage.setItem('domainID', id);
      // Assuming there's some React context or state management for $rootScope.currentDomain
      // For demonstration, using a global variable (not recommended in production)
      window.$rootScope.currentDomain = domain;
    } catch (error) {
      console.error(error);
    }
  }

  private static getAll(): AxiosPromise<Domain[]> {
    return axios.get('/api/domains'); // Replace with actual API endpoint
  }
}

export default DomainService;