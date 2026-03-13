import { Notification } from '@/components/Notification'; // Assuming Notification is a custom component for notifications

export class HelpersService {
    static showStandardMessages(response: any): void {
        if (response?.error) {
            Notification.error(response.error);
        }
        if (response?.warnings && Array.isArray(response.warnings)) {
            response.warnings.forEach((warning: string) => {
                Notification.warning(warning);
            });
        }
    }
}