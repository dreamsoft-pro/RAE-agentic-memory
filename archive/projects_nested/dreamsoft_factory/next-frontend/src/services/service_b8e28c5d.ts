import api from "@/lib/api";

class DpUserAddressService {

  private resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  public createAddress(data: any): Promise<any> {
    return new Promise((resolve, reject) => {
      const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`;
      api.post(url, data)
        .then(response => {
          if (response.data.response) {
            resolve(response.data);
          } else {
            reject(response.data);
          }
        })
        .catch(error => {
          reject(error);
        });
    });
  }

  public edit(data: any): Promise<any> {
    return new Promise((resolve, reject) => {
      const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`;
      api.put(url, data)
        .then(response => {
          if (response.data.response) {
            resolve(response.data);
          } else {
            reject(response.data);
          }
        })
        .catch(error => {
          reject(error);
        });
    });
  }

}