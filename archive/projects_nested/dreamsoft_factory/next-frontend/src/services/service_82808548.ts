import api from '@/lib/api'; // Custom axios import

class SubcategoryDescriptionsService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    setDescriptionFile(file: any): Promise<any> {
        return new Promise((resolve, reject) => {
            api.patch(`${this.resource}/files`, file)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }

    getDescriptionFile(descID: string): Promise<any> {
        return new Promise((resolve, reject) => {
            api.get(`${this.resource}/descFiles/${descID}`)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }
}

// Usage example
const service = new SubcategoryDescriptionsService('yourResourceName');
service.setDescriptionFile(yourFile)
    .then(data => console.log(data))
    .catch(error => console.error(error));

service.getDescriptionFile('someDescriptionID')
    .then(data => console.log(data))
    .catch(error => console.error(error));