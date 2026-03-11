import api from '@/lib/api';

class ConnectOptionService {

    static setPrice(connect: any, params: any) {
        return new Promise((resolve, reject) => {
            const resource = connect.resource;
            const url = `${process.env.API_URL}/${[resource, 'setPrice', connect.ID].join('/')}`;
            
            api.patch(url, params)
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

    static addToGroup(option: any, params: any) {
        return new Promise((resolve, reject) => {
            const resource = option.resource;
            const url = `${process.env.API_URL}/${[resource, 'addToGroup', option.ID].join('/')}`;

            api.patch(url, params)
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

export default ConnectOptionService;