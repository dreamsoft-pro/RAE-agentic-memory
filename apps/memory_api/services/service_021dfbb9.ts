import { useEffect, useState } from 'react';
import api from '@/lib/api';

interface Volume {
    volume: string;
    active: boolean;
}

const getActiveVolume = (volumes: Volume[], index: number): Volume | undefined => {
    const actVolume = volumes[index];

    if (actVolume) {
        if (!actVolume.active) {
            return getActiveVolume(volumes, index + 1);
        } else {
            return actVolume;
        }
    } else {
        console.error('Problem with realization time!');
        return undefined;
    }
};

const getActiveVolumeByVolume = async (volumes: Volume[], volume: string): Promise<Volume | undefined> => {
    const volumeIndex = volumes.findIndex(vol => vol.volume === volume);

    if (volumeIndex > -1) {
        if (!volumes[volumeIndex].active) {
            return getActiveVolume(volumes, volumeIndex + 1);
        } else {
            return volumes[volumeIndex];
        }
    } else {
        console.error('Problem with realization time!');
        return undefined;
    }
};

const MyComponent = () => {
    const [volumes, setVolumes] = useState<Volume[]>([]);
    const [activeVolume, setActiveVolume] = useState<Volume | null>(null);

    useEffect(() => {
        api.getVolumes().then(data => setVolumes(data));
    }, []);

    useEffect(() => {
        if (volumes.length > 0) {
            getActiveVolumeByVolume(volumes, 'some_volume')
                .then(activeVol => setActiveVolume(activeVol))
                .catch(error => console.error('Failed to find active volume:', error));
        }
    }, [volumes]);

    return (
        <div>
            {activeVolume ? (
                <div>
                    Active Volume: {activeVolume.volume}
                </div>
            ) : (
                <div>No active volume found</div>
            )}
        </div>
    );
};

export default MyComponent;