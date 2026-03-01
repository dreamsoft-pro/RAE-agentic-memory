import axios, { AxiosResponse } from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class DpAddressService {
  private apiUrl: string;

  constructor() {
    this.apiUrl = process.env.API_URL || '';
  }

  async deleteAddress(addressID: number): Promise<AxiosResponse> {
    return axios.delete(`${this.apiUrl}/resource/${addressID}`).then(response => response).catch(error => {
      throw error;
    });
  }
}

export default DpAddressService;