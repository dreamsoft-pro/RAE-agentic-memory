// In your component or service file

import api from "@/lib/api";

class ImageEffectService {
    private original: { height: number; width: number; outerHeight: number; outerWidth: number };
    private factor: { x: number; y: number };
    private mode: string;

    constructor(original: { height: number; width: number; outerHeight: number; outerWidth: number }, factor: { x: number; y: number }, mode: string) {
        this.original = original;
        this.factor = factor;
        this.mode = mode;
    }

    async applyEffect(o?: any, el?: HTMLElement): Promise<void> {
        const options = {
            from: o?.from || (this.mode === "show" ? {
                height: 0,
                width: 0,
                outerHeight: 0,
                outerWidth: 0
            } : this.original),
            to: {
                height: this.original.height * this.factor.y,
                width: this.original.width * this.factor.x,
                outerHeight: this.original.outerHeight * this.factor.y,
                outerWidth: this.original.outerWidth * this.factor.x
            }
        };

        if (o?.fade) {
            if (this.mode === "show") {
                options.from.opacity = 0;
                options.to.opacity = 1;
            }
            if (this.mode === "hide") {
                options.from.opacity = 1;
                options.to.opacity = 0;
            }
        }

        el?.effect(options);
    }

    async fetchData(): Promise<void> {
        try {
            const response = await api.get('/some-endpoint');
            console.log(response.data);
        } catch (error) {
            console.error('Failed to fetch data', error);
        }
    }
}

// Usage in a component
export default function ImageEffectComponent() {
    // Assuming you're rendering an image element and have the original dimensions, factor, mode available.
    const imageEffectService = new ImageEffectService(originalDimensions, { x: 1.5, y: 1.5 }, "show");

    return (
        <div>
            {/* Render some UI elements */}
            <button onClick={async () => await imageEffectService.fetchData()}>Fetch Data</button>
        </div>
    );
}