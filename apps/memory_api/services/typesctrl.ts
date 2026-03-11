// --- FILE: marginController.ts ---
import { MarginsService, Notification } from '@/services';
import api from '@/lib/api';

class MarginController {
    $scope = {
        cancel: this.cancel,
        removeMargin: this.removeMargin,
    };

    constructor(private $modalInstance: any, private $filter: any) {}

    cancel() {
        this.$modalInstance.close();
    }

    async removeMargin(marginID: string) {
        try {
            const data = await MarginsService.removeMargin(marginID);
            if (data.response) {
                Notification.success(this.$filter('translate')('success'));
                await api.loadMargins(); // Assuming loadMargins is a function that loads margins from API
            } else {
                Notification.error(this.$filter('translate')('error'));
            }
        } catch (error) {
            Notification.error(this.$filter('translate')('error'));
        }
    }

    $onInit() {}
}

export default MarginController;

// --- FILE: marginService.ts ---
import api from '@/lib/api';

class MarginsService {
    async removeMargin(marginID: string): Promise<any> {
        return await api.removeMargin(marginID);
    }
}

export { MarginsService };

// --- FILE: notificationService.ts ---
class Notification {
    success(message: string) {
        console.log(`Success: ${message}`);
    }

    error(message: string) {
        console.error(`Error: ${message}`);
    }
}

export default Notification;

// --- FILE: api.ts ---
import axios from 'axios';

const API_URL = '/api/margins'; // Example URL, adjust accordingly

class ApiClient {
    private httpClient = axios.create({
        baseURL: API_URL,
    });

    async loadMargins() {
        try {
            const response = await this.httpClient.get('');
            return response.data;
        } catch (error) {
            throw new Error('Failed to load margins');
        }
    }

    // [BACKEND_ADVICE] This logic belongs in the PHP API
    async removeMargin(marginID: string): Promise<any> {
        try {
            const response = await this.httpClient.delete(`/${marginID}`);
            return response.data;
        } catch (error) {
            throw new Error('Failed to remove margin');
        }
    }
}

export default new ApiClient();

// --- FILE: marginHooks.ts ---
import { useApi, useState } from '@/hooks';

function useMargins() {
    const [margins, setMargins] = useState([]);
    const api = useApi();

    async function loadMargins() {
        try {
            const marginsData = await api.loadMargins();
            setMargins(marginsData);
        } catch (error) {
            console.error(error.message);
        }
    }

    return { margins, loadMargins };
}

export default useMargins;

// --- FILE: marginUtils.ts ---
function translateSuccessMessage($filter: any) {
    return $filter('translate')('success');
}

function translateErrorMessage($filter: any) {
    return $filter('translate')('error');
}

export { translateSuccessMessage, translateErrorMessage };