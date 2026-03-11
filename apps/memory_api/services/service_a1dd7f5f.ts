import api from '@/lib/api';
import { Notification } from '@/components/UI'; // Assuming Notification is a custom component or service

class PsTypeController {
    private refreshTypes: () => void;

    constructor(refreshTypesFn: () => void) {
        this.refreshTypes = refreshTypesFn;
    }

    async copy(typeID: string): Promise<void> {
        try {
            const response = await api.post('/api/types/copy', { typeID });
            if (response.data.response) {
                Notification.success('copied_successful');
                this.refreshTypes();
            } else {
                Notification.error('error');
            }
        } catch (error) {
            console.error('Failed to copy type:', error);
            Notification.error('An unexpected error occurred');
        }
    }

    async saveQuestionOnly(isQuestionOnly: boolean, typeID: string): Promise<void> {
        try {
            const response = await api.post('/api/types/save-question-only', { currentGroupID, isQuestionOnly, typeID });
            if (response.data.response) {
                Notification.success('updated');
                this.refreshTypes();
            } else {
                Notification.error('error');
            }
        } catch (error) {
            console.error('Failed to save question only:', error);
            Notification.error(error.message || 'An unexpected error occurred');
        }
    }

    // This method is a placeholder for the actual implementation of refreshTypes
    private refreshTypes(): void {
        throw new Error("Method 'refreshTypes' must be implemented by the consumer");
    }
}