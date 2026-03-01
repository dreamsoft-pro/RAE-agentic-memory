import api from '@/lib/api';

class PsPreflightFolderService {

    private resource: string; // Ensure this variable is defined before use
    private contentID: string | number; // Ensure this variable is defined before use

    remove(item: { ID: string | number }) {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/${item.ID}`;

        return api.delete(url)
            .then(data => {
                if (data.response) {
                    cache.remove(this.contentID);
                    return data;
                } else {
                    throw new Error(JSON.stringify(data));
                }
            })
            .catch(error => {
                throw error;
            });
    }

    // Ensure you define and initialize resource and contentID somewhere in your class
}

// Example usage:
const service = new PsPreflightFolderService();
service.resource = 'folders'; // Define this before using the remove method
service.contentID = 123; // Define this before using the remove method

service.remove({ ID: 456 })
    .then(result => console.log('Success:', result))
    .catch(error => console.error('Error:', error));