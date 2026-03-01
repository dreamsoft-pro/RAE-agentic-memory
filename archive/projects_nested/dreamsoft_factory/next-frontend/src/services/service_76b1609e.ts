import api from '@/lib/api';
import { useEffect } from 'react';

interface FilesData {
    files: File[];
    descID?: string;
}

const CategoryDescriptionsService = {
    setDescriptionFile: async (filesData: FilesData): Promise<void> => {
        try {
            await api.post('/api/set-description-file', filesData);
        } catch (error) {
            console.error('Error setting description file:', error);
        }
    },
};

export default function CategoryDescription() {
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
    const [currentDescID, setCurrentDescID] = useState<string | null>(null);

    useEffect(() => {
        // Assuming selectedFiles and currentDescID are set somewhere in your application
    }, []);

    const setDescriptionFile = async () => {
        if (!selectedFiles || !currentDescID) return;

        try {
            await CategoryDescriptionsService.setDescriptionFile({
                files: selectedFiles,
                descID: currentDescID,
            });
            Notification.success('success');
        } catch (error) {
            console.error('Failed to set description file:', error);
        }
    };

    const removeDescFile = async (fileID: string) => {
        // Implement the logic for removing a description file
    };

    const removeFile = async (categoryService, categoryType, file) => {
        // Implement the logic for removing a file from the category service
    };

    return (
        <form>
            {/* Render your form elements here */}
            <button type="button" onClick={setDescriptionFile}>Save Description Files</button>
            <button type="button" onClick={() => removeDescFile('fileID')}>Remove Description File</button>
        </form>
    );
}