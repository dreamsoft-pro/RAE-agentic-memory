javascript
import { API } from '@/lib/api';

class DpUserAddressService {
  constructor(userID) {
    this.userID = userID;
    this.resource = ['users', this.userID, 'address'].join('/');
  }

  // [BACKEND_ADVICE] Heavy logic here.
  getAllAddresses() {
    return new Promise((resolve, reject) => {
      API.get(`${this.resource}?type=1`)
        .then(response => resolve(response.data))
        .catch(error => reject(error));
    });
  }

  // [BACKEND_ADvice] Heavy logic here.
  getAllAddressesVat() {
    return new Promise((resolve, reject) => {
      API.get(`${this.resource}?type=2`)
        .then(response => resolve(response.data))
        .catch(error => reject(error));
    });
  }
}

export default DpUserAddressService;
