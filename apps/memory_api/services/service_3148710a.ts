import api from '@/lib/api';
import { useEffect, useState } from 'react';

class EffectBounce {
    private el: HTMLElement;
    private mode: string = "effect";
    private direction: string = "up";
    private distance: number = 20; // Default value if not provided in constructor
    private times: number = 5;
    private duration: number = 1000;

    constructor(el: HTMLElement, options?: { mode?: string, direction?: string, distance?: number, times?: number, duration?: number }) {
        this.el = el;
        if (options) {
            Object.assign(this, options);
        }
    }

    private setMode(mode: string): string {
        return mode; // Simplified version of the method from jQuery UI
    }

    public async executeEffect(): Promise<void> {
        const hide = this.mode === "hide";
        const show = this.mode === "show";

        let anims = this.times * 2 + (show || hide ? 1 : 0);
        const speed = this.duration / anims;

        // Assume we are working with a simple effect and not actual DOM manipulation
        for (let i = 0; i < anims; i++) {
            await new Promise(resolve => setTimeout(resolve, speed));
            console.log(`Animation step ${i + 1}`);
        }
    }

    public async fetchData() {
        try {
            const response = await api.get('/some-endpoint');
            console.log(response.data);
        } catch (error) {
            console.error('Failed to fetch data', error);
        }
    }
}

// Example usage in a React component
const MyComponent: React.FC = () => {
    const [effectInstance, setEffectInstance] = useState<EffectBounce | null>(null);

    useEffect(() => {
        const el = document.getElementById("my-element")!;
        const effect = new EffectBounce(el);
        setEffectInstance(effect);

        effect.executeEffect();
        effect.fetchData();

        return () => {
            // Cleanup if needed
        };
    }, []);

    return <div id="my-element">My Element</div>;
};

export default MyComponent;