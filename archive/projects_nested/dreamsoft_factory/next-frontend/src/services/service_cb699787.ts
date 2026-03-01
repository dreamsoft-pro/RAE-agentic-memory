import api from '@/lib/api';

export class UtilityClass {
    private static async getDateByWorkingDays(days: number): Promise<Date> {
        const response = await api.workingDayCalculator.getWorkingDate(days);
        return new Date(response.date);
    }

    public static addDaysToDate(days: number, currentDate: string | Date): Date {
        const dateObj = new Date(currentDate);
        dateObj.setDate(dateObj.getDate() + days);
        return dateObj;
    }

    public static compareDates(date1: string | Date, date2: string | Date): boolean {
        if (!date1) {
            return false;
        }
        const dateOne = new Date(date1);
        const dateTwo = new Date(date2);
        return dateOne > dateTwo;
    }

    public static async getOrderMessages(orderID: number): Promise<void> {
        try {
            const data = await api.orderMessageService.getMessages(orderID);
            // Assuming you have a way to set the messages, for example in a component state
            this.setOrderMessages(data); 
        } catch (error) {
            console.error('Failed to get order messages:', error);
        }
    }

    private static setOrderMessages(messages: any[]): void {
        // This method should be implemented based on your application logic.
        // For example, in a React component state setter or similar context
    }
}