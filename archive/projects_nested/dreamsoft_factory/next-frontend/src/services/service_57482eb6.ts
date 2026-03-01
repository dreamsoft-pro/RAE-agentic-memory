import api from "@/lib/api";

class AuthService {
    private setUserData(data: any): Promise<any> {
        // Implementation of the setUserData method.
        return new Promise((resolve, reject) => {
            try {
                // Set user data logic here...
                resolve(true);
            } catch (error) {
                reject(error);
            }
        });
    }

    public checkAuth(): Promise<any> {
        const url = `${process.env.API_URL}/auth/check`;

        return api.get(url).then((response: any) => {
            if (response.data.response) {
                this.setUserData(response.data).then(confirm => response.data);
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        }).catch(error => {
            throw error;
        });
    }

    public addToCart(params: any): Promise<any> {
        const url = `${process.env.API_URL}/cart/add`; // Assuming the endpoint is '/cart/add' for adding to cart

        return api.post(url, params).then((response: any) => {
            if (response.data.success) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        }).catch(error => {
            throw error;
        });
    }

    // Add other methods here as needed.
}