import api from '@/lib/api';

class CustomVolumeController {
    private customVolume: any;
    private volumes: any[];
    private notificationService: any;

    constructor(customVolume: any, volumes: any[], notificationService: any) {
        this.customVolume = customVolume || {};
        this.volumes = volumes || [];
        this.notificationService = notificationService;
    }

    public async addNewVolume() {
        if (this.customVolume.newVolume === undefined) {
            this.customVolume.newVolume = this.customVolume.minVolume ?? 0; // Default to 0 if minVolume is not defined
            await this.notificationService.error('incorrect_volume');
            return;
        }

        const newVolume: { volume: number, active: boolean } = { volume: this.customVolume.newVolume, active: true };
        
        if (!this.customVolume.volumes) {
            this.customVolume.volumes = [];
        }
        
        let idxV = this.volumes.findIndex(volume => volume.volume === this.customVolume.newVolume);
        let idxCV = this.customVolume.volumes.findIndex(volume => volume.volume === this.customVolume.newVolume);

        if (idxV === -1 && idxCV === -1) {
            // Proceed with adding new volume logic here
        }
    }
}