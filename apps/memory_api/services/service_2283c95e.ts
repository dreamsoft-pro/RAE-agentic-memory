import api from '@/lib/api';
import { defer } from 'node:util';

class FileService {
    private async getAggregateOrders(ordersData): Promise<any[]> {
        // Mock implementation for demonstration purposes.
        return new Promise((resolve) => setTimeout(() => resolve([]), 100));
    }

    private async getByList(orders: any[]): Promise<any> {
        // Mock implementation for demonstration purposes.
        return new Promise((resolve) => setTimeout(() => resolve([]), 100));
    }

    public async getAllFiles(ordersData): Promise<any[]> {
        const orders = await this.getAggregateOrders(ordersData);
        const data = await this.getByList(orders);
        return data;
    }

    public removeFile(product, file) {
        const fileIdx = product.fileList.findIndex(f => f.ID === file.ID);
        if (fileIdx > -1) {
            const toRemove = { ...product.fileList[fileIdx] };
            product.fileList.splice(fileIdx, 1);
            if (product.lastFile && toRemove.ID === product.lastFile.ID) {
                product.lastFile = this.getLastFile(product);
            }
        }
        return product;
    }

    private getLastFile(product): any | null {
        const sortedFiles = [...product.fileList].sort((a, b) => a.created - b.created);
        return sortedFiles.length > 0 ? sortedFiles[sortedFiles.length - 1] : null;
    }

    public mergeFiles(ordersData): void {
        // Assuming this function does not need to be asynchronous and it's logic is unclear from the snippet.
        // Implement business logic here if needed.
    }
}

export default FileService;

// Example usage:
const fileService = new FileService();
fileService.getAllFiles({ /* orders data */ })
  .then(data => console.log('Fetched files:', data))
  .catch(error => console.error('Error fetching files:', error));