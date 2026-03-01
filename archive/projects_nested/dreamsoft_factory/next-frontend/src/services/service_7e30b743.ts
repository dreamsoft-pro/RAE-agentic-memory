import api from '@/lib/api';
import { Notification } from '@/components/UI'; // Assuming the existence of a notification component

class ProductController {
    private resource: string; // Define this in your constructor or wherever appropriate
    private url: string; // Define this in your constructor or wherever appropriate
    private product: any; // Replace 'any' with an actual type if possible
    private minPages: number;
    private maxPages: number;

    async updateCurrentPages(pages: number) {
        if (pages > this.maxPages) {
            Notification.info(`maximum_number_of_pages ${this.maxPages}`);
            this.product.currentPages = this.maxPages;
            pages = this.maxPages;
        } else if (pages < this.minPages) {
            Notification.info(`minimum_number_of_pages ${this.minPages}`);
            this.product.currentPages = this.minPages;
            pages = this.minPages;
        } else if (typeof pages === 'undefined') {
            Notification.info(`range_of_pages ${this.minPages} - ${this.maxPages}`);
        } else {
            this.product.currentPages = pages;
        }
    }

    // Add a constructor or initialization method to set up your properties
}