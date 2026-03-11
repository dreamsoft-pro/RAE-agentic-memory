import api from "@/lib/api";

class ExampleClass {
    private resource: string;
    private url: string;

    constructor(resource: string, url: string) {
        this.resource = resource;
        this.url = url;
    }

    public async createNewItem(amount: number, volume?: number): Promise<void> {
        const newItem: { amount: number; volume?: number } = { amount };

        if (volume !== undefined) {
            newItem.volume = volume;
        }

        try {
            await api.post(this.url, newItem);
        } catch (error) {
            console.error("Failed to create new item:", error);
        }
    }
}