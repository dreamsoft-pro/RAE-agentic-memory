import api from "@/lib/api";
import { useState } from "react";

class MyFileHandler {
    constructor(private scope: any, private notificationService: NotificationService) {}

    async getThumbsModal($scope: any): Promise<void> {
        const resource = 'thumbs';
        try {
            const response = await api.get(`/${resource}`);
            this.notificationService.success('deleted_successful');  // Assuming there's a success message key
        } catch (error) {
            console.error(error);
            this.notificationService.error('error');
        }
    }

    removeDescFile(fileID: string): void {
        const idx = this.scope.selectedFiles.findIndex((file: { ID: string }) => file.ID === fileID);
        if(idx > -1) {
            this.scope.selectedFiles.splice(idx, 1);
        }
    }

    addFilesToView(destination: string, data: any): void {
        if (this.scope[destination]) {
            this.scope[destination].push(data.item);
        } else {
            console.error(`Destination ${destination} not found in scope.`);
        }
    }
}

interface NotificationService {
    success(message: string): void;
    error(message: string): void;
}