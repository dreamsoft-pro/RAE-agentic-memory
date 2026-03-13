import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

interface Config {
  API_URL: string;
}

class DpAddressService {
  private static apiConfig: Config;

  public static setAddressConfig(config: Config) {
    this.apiConfig = config;
  }

  public static addAddress(resource: string, type: string, data: any): Promise<any> {
    return axios.post(`${this.apiConfig.API_URL}${resource}/addAddress/${type}`, data).then((response) => response.data)
      .catch((error) => { throw error; });
  }

  public static emptyAddress(resource: string): Promise<any> {
    return axios.get(`${this.apiConfig.API_URL}${resource}/emptyAddress`).then((response) => response.data)
      .catch((error) => { throw error; });
  }
}

// Usage
const config = { API_URL: 'http://example.com/api' };
DpAddressService.setAddressConfig(config);

DpAddressService.addAddress('someResource', 'type', {}).then(data => console.log(data))
  .catch(error => console.error(error));

DpAddressService.emptyAddress('anotherResource').then(data => console.log(data))
  .catch(error => console.error(error));