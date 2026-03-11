import axios from '@api'; // Assuming @/lib/api is properly set up as an Axios instance

class PictureUploader {
    selectedFiles: any[] = []; // Define the structure or type based on actual data

    addPicture(elem: { ID: number }, currentDescID?: string): void {
        const idx = this.selectedFiles.findIndex(file => file.ID === elem.ID);
        if (idx > -1) {
            console.log('duplicate');
        } else {
            this.selectedFiles.push(elem);
        }
    }

    async uploadFile(scope: any, service: string, filesKey: string): Promise<void> {
        const formData = new FormData();
        scope[filesKey].forEach(file => {
            formData.append(`thumbFiles[]`, file);
        });

        try {
            await axios.post('/api/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        } catch (error) {
            console.error('Error uploading files:', error);
        }
    }

    async savePictures(currentDescID?: string): Promise<void> {
        const data = JSON.stringify({ selectedFiles: this.selectedFiles });

        try {
            await axios.post('/api/save', { picturesData: data });
        } catch (error) {
            console.error('Error saving pictures:', error);
        }
    }
}

// Usage Example:
const uploaderInstance = new PictureUploader();

uploaderInstance.addPicture({ ID: 123, name: 'file.jpg' });

uploaderInstance.uploadFile($scope, 'service', 'thumbFiles').then(() => {
    uploaderInstance.savePictures().catch(error => console.error('Failed to save pictures:', error));
});