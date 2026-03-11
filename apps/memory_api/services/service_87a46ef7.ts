import api from '@/lib/api';

export default class MarginsLoader {
    private selectedPriceListID: string | null = null;
    private selectedNatureID: string | null = null;
    private currentGroupID: string;

    constructor(selectedPriceListID: string, selectedNatureID: string, currentGroupID: string) {
        this.selectedPriceListID = selectedPriceListID;
        this.selectedNatureID = selectedNatureID;
        this.currentGroupID = currentGroupID;
    }

    public async loadMargins(): Promise<void> {
        if (!this.selectedPriceListID || !this.selectedNatureID) {
            return;
        }
        
        try {
            const data = await api.get(`/margins/${this.selectedPriceListID}/${this.selectedNatureID}/${this.currentGroupID}`);
            this.margins = data; // Assuming 'margins' is a property of the class
        } catch (error) {
            console.error('Failed to load margins:', error);
        }
    }

    private margins: any[] = []; // Example type, replace with actual type if known

    getMargins(): any[] {
        return this.margins;
    }
}