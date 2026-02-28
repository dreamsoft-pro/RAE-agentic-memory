import api from '@/lib/api';
import { findIndex } from 'lodash';

class VolumeHandler {
    private volumes: any[] = [];
    private productItem: any = {};
    private realisationTimes: any[] = [];

    async updateVolume(actVolume: any, volume: any) {
        const idxVol = findIndex(this.volumes, { volume: actVolume.volume });

        if (idxVol !== -1) {
            this.volumes[idxVol].active = actVolume.active;
        }

        this.productItem.volume = volume.volume;

        this.realisationTimes.forEach((realisationTime, rIndex) => {
            const idxVol = findIndex(realisationTime.volumes, { volume: volume.volume });
            if (idxVol !== -1) {
                realisationTime.volumes[idxVol].active = realisationTime.volumes[idxVol].active;
            }
        });
    }

    // Assuming there's a method to fetch volumes or realisationTimes from API
    async fetchData() {
        try {
            const [volumesResponse, productItemResponse] = await Promise.all([
                api.get('/api/v1/volumes'),
                api.get('/api/v1/product-item')
            ]);

            this.volumes = volumesResponse.data;
            this.productItem = productItemResponse.data;

            return { volumes: this.volumes, productItem: this.productItem };
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    // Example usage
    async exampleUsage() {
        await this.fetchData();
        
        const actVolume = { volume: 'example-volume', active: true };
        const volume = { volume: 'another-example-volume' };

        await this.updateVolume(actVolume, volume);

        console.log(this.volumes);
        console.log(this.productItem);
    }
}

// Usage
const handler = new VolumeHandler();
handler.exampleUsage().then(() => console.log('Done'));