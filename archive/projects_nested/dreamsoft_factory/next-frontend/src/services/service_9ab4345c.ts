import api from '@/lib/api';
import { useState } from 'react';

class CustomVolumeController {
    private customVolume: CustomVolumeModel = {
        maxVolume: '0',
        minVolume: '0',
        newVolume: '0'
    };

    async validateAndSetNewVolume(): Promise<void> {
        try {
            const { maxVolume, minVolume, newVolume } = this.customVolume;

            if (parseInt(maxVolume) < parseInt(newVolume)) {
                this.customVolume.newVolume = maxVolume;
                await this.showError('to_high_volume', maxVolume);
                return;
            }

            if (parseInt(minVolume) > parseInt(newVolume)) {
                this.customVolume.newVolume = minVolume;
                await this.showError('to_low_volume', minVolume);
                return;
            }
        } catch (error) {
            console.error(error);
        }
    }

    private async showError(messageKey: string, value: string): Promise<void> {
        // Assuming Notification and translate function are available as services or hooks.
        const errorMessage = `Error: ${messageKey} - ${value}`;
        await this.notify(errorMessage); // Implement notify method for notification service
    }

    private async notify(message: string): Promise<void> {
        // Implementation of the actual notification logic
        console.log('Notification:', message);
    }
}

interface CustomVolumeModel {
    maxVolume: string;
    minVolume: string;
    newVolume: string;
}