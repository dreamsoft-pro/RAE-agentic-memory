javascript
import { api } from '@/lib/api';
import { inject } from 'inversify';

@inject('$rootScope', '$q', '$config', '$injector')
export class TokenService {
    @BACKEND_ADVICE check = () => {
        const def = this.$q.defer();

        this.$http.get(`${this.$config.API_URL}/auth/check`)
            .then((response) => {
                if (response.data.response) {
                    def.resolve(response.data);
                } else {
                    def.reject(response.data);
                }
            })
            .catch((error) => {
                def.reject(error);
            });

        return def.promise;
    };

    @BACKEND_ADVICE getNonUserToken = () => {
        const def = this.$q.defer();

        this.$http.get(`${this.$config.API_URL}/auth/non-user-token`)
            .then((response) => {
                def.resolve(response.data);
            })
            .catch((error) => {
                def.reject(error);
            });

        return def.promise;
    };
}
