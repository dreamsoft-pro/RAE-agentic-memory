import { useCallback } from 'react';
import axios from '@/lib/api'; // Assuming this is an Axios instance wrapper

class RealizationTimesController {
    private realisationTimes: any[] = [];
    private rememberVolume: any = {};

    constructor(realisationTimes: any[], rememberVolume: any) {
        this.realisationTimes = realisationTimes;
        this.rememberVolume = rememberVolume;
    }

    public async checkRealisationTime(): Promise<void> {
        const idxRT = this.findIndex(this.realisationTimes, 'ID', this.rememberVolume.realisationTime.ID);
        if (idxRT !== -1) {
            const idxVol = this.findIndex(this.realisationTimes[idxRT].volumes, 'volume', this.rememberVolume.volume.volume);
            if (idxVol !== -1) {
                await this.checkVolume(this.realisationTimes[idxRT], this.realisationTimes[idxRT].volumes[idxVol]);
            } else {
                await this.checkVolume(this.realisationTimes[0], this.realisationTimes[0].volumes[0]);
            }
        }
    }

    private async checkVolume(realisationTime: any, volume: any): Promise<void> {
        // Implement your logic here
    }

    private findIndex(array: any[], key: string, value: any): number {
        return array.findIndex(item => item[key] === value);
    }
}