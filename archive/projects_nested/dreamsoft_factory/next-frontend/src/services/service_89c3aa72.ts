javascript
import api from '@/lib/api';

class TypeService {
  static getTypesData(typesList) {
    const def = new Promise((resolve, reject) => {
      api.post('/ps_types/getTypesData', { types: typesList }).then(resolve).catch(reject);
    });

    return def;
  }

  static search(text) {
    const def = new Promise((resolve, reject) => {
      api.get(`/ps_types/search/${text}`).then(resolve).catch(reject);
    });

    return def;
  }
}