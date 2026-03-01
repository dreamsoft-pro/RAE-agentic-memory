import api from '@/lib/api';
import { setCookie } from 'js-cookie'; // Assuming js-cookie for setting cookies in Next.js

class MainWidgetService {
    static async copyAddressesToNewProduct(product: any, savedProduct: any) {
        const def = this.defer(); // This function should be defined elsewhere or assumed to exist
        try {
            if (savedProduct.customVolumes) {
                setCookie('customVolumes', JSON.stringify(savedProduct.customVolumes), { expires: 7 }); // Assuming days as the duration

                await api.post('/api/update-product', { product, customVolumes: savedProduct.customVolumes });
            } else {
                throw new Error('Volume does not exist');
            }
        } catch (error) {
            console.error(error);
            this.notifyError('volume_exist'); // This function should be defined elsewhere or assumed to exist
        } finally {
            def.resolve();
        }
    }

    static defer() {
        return Promise.resolve(); // Simplified for example, actual implementation may differ
    }

    static notifyError(message: string) {
        console.error(`Notification error: ${message}`); // Placeholder function
    }
}