import api from '@/lib/api';

class AuthService {
    private setUserData(data: any): Promise<any> {
        // Implement this method based on your logic
        return new Promise((resolve, reject) => {
            resolve(true); // Placeholder
        });
    }

    login(credentials: any): Promise<any> {
        const resource = 'login';
        const url = `${process.env.AUTH_URL}/${resource}`;
        
        return api.post(url, $.param(credentials), {
            params: {
                domainName: this.domainHost,
            },
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            }
        }).then((response) => {
            return this.setUserData(response.data).then(confirmResult => {
                if (confirmResult) {
                    return response.data;
                } else {
                    throw confirmResult; // Reject the promise
                }
            });
        }).catch(error => {
            throw error;
        });
    }

    logout(): Promise<void> {
        const url = `${process.env.AUTH_URL}/logout`; // Assuming there's a '/logout' endpoint

        return api.post(url).then(() => {
            // Perform any necessary cleanup, such as clearing user data
            this.clearUserData();
            return Promise.resolve(); // Resolve the promise
        }).catch(error => {
            throw error; // Reject the promise with an error
        });
    }

    private clearUserData(): void {
        // Implement logic to clear user data here
    }
}