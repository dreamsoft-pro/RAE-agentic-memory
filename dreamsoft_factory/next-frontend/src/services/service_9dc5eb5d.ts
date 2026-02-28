import api from '@/lib/api';
import { useState, useEffect } from 'react';

interface SettingService {
    getSkinName(): Promise<{ skinName: string }>;
    getPublicSettings(): Promise<any>;
}

const settingService = (name: string): SettingService => ({
    async getSkinName() {
        const response = await api.get(`/setting/${name}/skin`);
        return { skinName: response.data.skin };
    },
    async getPublicSettings() {
        const response = await api.get(`/setting/${name}/public`);
        return response.data;
    }
});

const SettingComponent = () => {
    const [skinName, setSkinName] = useState('');
    const [formsData, setFormsData] = useState(null);

    useEffect(() => {
        (async () => {
            try {
                const skinSettingService = settingService('general');
                const { skinName: fetchedSkinName } = await skinSettingService.getSkinName();
                setSkinName(fetchedSkinName);
                
                const formsSettingService = settingService('forms');
                const fetchedFormsData = await formsSettingService.getPublicSettings();
                setFormsData(fetchedFormsData);
            } catch (error) {
                console.error("Error fetching settings:", error);
            }
        })();
    }, []);

    return (
        <div>
            {/* Render your component here */}
            <p>Skin Name: {skinName}</p>
            <pre>{JSON.stringify(formsData, null, 2)}</pre>
        </div>
    );
};

export default SettingComponent;

// Utility function for formatting size units (not used in the component above)
function formatSizeUnits(bytes: number): string {
    if (bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}