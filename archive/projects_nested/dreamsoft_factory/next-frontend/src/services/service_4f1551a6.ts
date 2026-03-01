import api from '@/lib/api';

class VolumeManager {
    private customVolume: any;
    private rememberVolume: any;
    private productItem: any;
    private currentTypeID: string | number;
    private newVolume: any;

    constructor(customVolume: any, rememberVolume: any, productItem: any, currentTypeID: string | number) {
        this.customVolume = customVolume;
        this.rememberVolume = rememberVolume;
        this.productItem = productItem;
        this.currentTypeID = currentTypeID;
    }

    async manageVolumes(newVolume: any): Promise<void> {
        this.newVolume = newVolume;

        // Add new volume to custom volumes
        this.customVolume.volumes.push(this.newVolume);
        this.rememberVolume.volume = this.newVolume;

        // Fetch custom volumes from cookie if exists
        const customVolumesFromCookie = await this.getCustomVolumesFromCookie();
        let cookieCustomVolumes: Record<string, any> = {};

        if (customVolumesFromCookie) {
            try {
                cookieCustomVolumes = JSON.parse(customVolumesFromCookie);
            } catch (error) {
                console.error('Failed to parse custom volumes from cookie:', error);
            }
        }

        // Ensure the currentTypeID exists in the cookieCustomVolumes
        if (!cookieCustomVolumes[this.currentTypeID]) {
            cookieCustomVolumes[this.currentTypeID] = this.customVolume;
        }

        console.log(JSON.stringify(cookieCustomVolumes));

        // Call getVolumes API with productItem.amount as parameter
        await this.getVolumes(this.productItem.amount);
    }

    private async getCustomVolumesFromCookie(): Promise<string | null> {
        return api.getCookie('customVolumes');
    }

    private async getVolumes(amount: number): Promise<void> {
        try {
            // Assuming there's an API call to fetch volumes
            const response = await api.getVolumesForAmount({ amount });
            console.log(response);
        } catch (error) {
            console.error('Failed to get volumes:', error);
        }
    }
}