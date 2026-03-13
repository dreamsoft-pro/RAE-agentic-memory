import api from "@/lib/api";
import { each } from "lodash";

class OrdersFetcher {
    private ordersData: any[]; // Ensure the type is properly defined according to your data structure

    constructor(ordersData: any[]) {
        this.ordersData = ordersData;
    }

    async fetchAllFiles() {
        try {
            const fetchedData = await api.getAllFiles(this.ordersData);
            each(this.ordersData, order => {
                if (order.products) {
                    order.filesAlert = order.products.length;
                    order.waitForAccept = order.products.length;

                    let filesRejected = 0;
                    let reportsToAccept = order.products.length; // Derived from business logic

                    each(order.products, product => {
                        if (product.accept === 1) {
                            reportsToAccept--;
                        } else if (product.accept === -1) {
                            filesRejected++;
                        }
                        product.fileList = [];
                        product.lastFile = {};
                        
                        // Update order properties based on product status
                        order.waitForAccept = reportsToAccept;
                        order.filesRejected = filesRejected;
                    });
                }

                order.reportsToAccept = 0; // Ensure this is consistent with logic above if needed
            });

        } catch (error) {
            console.error("Failed to fetch all files", error);
        }
    }
}