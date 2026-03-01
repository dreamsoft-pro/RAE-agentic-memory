import axios from 'axios';

class PhotoFolderService {
    static async edit(folder: { id: string; name: string; description?: string }) {
        const url = '<your-base-url>';
        const headers = { /* your headers */ };

        try {
            const response = await axios.put(
                `${url}folder/${folder.id}/`,
                {
                    parent: null,
                    folderName: folder.name,
                    description: folder.description || '',
                    date: Date.now()
                },
                { headers, crossDomain: true }
            );
            return response.data;
        } catch (error) {
            console.error('Failed to edit folder:', error);
            throw error;
        }
    }
}