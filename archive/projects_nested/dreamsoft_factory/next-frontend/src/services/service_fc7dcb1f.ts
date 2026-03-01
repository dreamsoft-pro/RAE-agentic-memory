import api from '@/lib/api';
import { Cache } from 'some-cache-library'; // Replace with actual cache library

export default class PsPreflightFolderService {
  private getAllResource: string;
  private formatID: number | string; // Adjust type as necessary
  private categoryID: number | string; // Adjust type as necessary
  private cache: Cache;

  constructor(categoryID: number | string, formatID: number | string) {
    this.categoryID = categoryID;
    this.formatID = formatID;
    this.cache = new Cache(); // Replace with actual instantiation of your cache library
  }

  public async getAll(force?: boolean): Promise<any> {
    let getAllDef = null;

    if (getAllDef === null || force) {
      getAllDef = { resolve: (value: any) => {}, reject: (reason: any) => {} };
    } else {
      return new Promise((resolve, reject) => {
        this.cache.get('collection', resolve, reject);
      });
    }

    if (this.cache.has(this.categoryID) && !force) {
      getAllDef.resolve = (value) => value;
      getAllDef.resolve(this.cache.get(this.categoryID));
    } else {
      try {
        const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}/${this.getAllResource}`);
        this.cache.put(this.categoryID, response.data);
        return Promise.resolve(response.data);
      } catch (error) {
        return Promise.reject(error);
      }
    }

    return new Promise((resolve, reject) => {
      getAllDef.resolve ? resolve(getAllDef.resolve()) : reject(getAllDef.reject());
    });
  }

  public add(item: any): void {
    item.formatID = this.formatID;
    
    // Replace with actual implementation
    api.post(`${process.env.NEXT_PUBLIC_API_URL}/${this.getAllResource}`, item)
      .then((response) => console.log(response))
      .catch((error) => console.error(error));
  }
}