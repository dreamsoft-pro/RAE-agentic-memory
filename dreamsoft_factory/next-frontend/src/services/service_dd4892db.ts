import api from '@/lib/api';

class ReclamationFaultService {
  private resource: string[];

  constructor(resource: string[]) {
    this.resource = resource;
  }

  public editFault(data: any): Promise<any> {
    return new Promise((resolve, reject) => {
      const url = `${process.env.API_URL}/${this.resource.join('/')}`;

      api.put(url, data)
        .then(response => {
          if (response.data.response) {
            resolve(response.data);
          } else {
            reject(response.data);
          }
        })
        .catch(error => {
          reject(error.response ? error.response.data : error.message);
        });
    });
  }
}

export default ReclamationFaultService;