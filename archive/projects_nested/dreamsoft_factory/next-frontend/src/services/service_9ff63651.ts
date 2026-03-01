import axios from 'axios';

class MyClass {
    async makeBook(folder: any): Promise<any> {
        const url = /* your base URL */;
        const header = /* your headers */;

        try {
            const response = await axios.post(
                `${url}folder/make-book/${folder._id}`,
                {
                    typeID: 44,
                    pages: 16,
                    formatID: 148,
                    folderID: folder._id,
                    attributes: {
                        i1: 34,
                        i2: 19,
                        i3: 40,
                        i4: 74,
                        i9: 119,
                        i26: 242
                    }
                },
                { headers: header, withCredentials: true }
            );
            return response.data;
        } catch (error) {
            throw error.response ? error.response.status : 'Request failed';
        }
    }
}