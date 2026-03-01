import api from '@/lib/api';

class MyClass {
    private async updateDefaultAddress(param: any): Promise<any> {
        const url = `${process.env.AUTH_URL}/cart/updateDefaultAddress`;
        
        try {
            const response = await api.post(url, $.param(param), {
                params: { domainName: location.hostname },
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });
            
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    // Example usage
    async performAction() {
        try {
            const result = await this.updateDefaultAddress({ someParam: 'value' });
            console.log(result);
        } catch (error) {
            console.error(error);
        }
    }
}