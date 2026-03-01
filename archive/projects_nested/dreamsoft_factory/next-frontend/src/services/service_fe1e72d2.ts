import api from '@/lib/api';

class AnimationHelper {
    private _normalizeArguments: (arg1: any, arg2?: any) => { mode: string };
    private standardAnimationOption: (option: any) => boolean;

    constructor(normalizeFn: (arg1: any, arg2?: any) => { mode: string }, standardCheckFn: (option: any) => boolean) {
        this._normalizeArguments = normalizeFn;
        this.standardAnimationOption = standardCheckFn;
    }

    hide(option: any): void | Promise<void> {
        if (this.standardAnimationOption(option)) {
            // Assuming there's an original function to call here, just return for demonstration.
            console.log('Calling original hide');
            return;
        } else {
            const args = this._normalizeArguments(option);
            args.mode = "hide";
            this.effect(args);
        }
    }

    toggle(option: any): void | Promise<void> {
        if (this.standardAnimationOption(option) || typeof option === 'boolean') {
            // Assuming there's an original function to call here, just return for demonstration.
            console.log('Calling original toggle');
            return;
        } else {
            const args = this._normalizeArguments(option);
            args.mode = "toggle";
            this.effect(args);
        }
    }

    private effect(args: { mode: string }): void | Promise<void> {
        // Placeholder method, replace with actual logic
        console.log('Effect called with:', args);
    }

    css(key: string): number[] {
        const styleValue = this.getStyleProperty(key);
        return this.cssUnit(styleValue);
    }

    private getStyleProperty(key: string): string {
        // Mock implementation for demonstration purposes.
        return '20px';
    }

    private cssUnit(value: string): number[] {
        const units = ["em", "px", "%", "pt"];
        let result: number[] | undefined;

        units.forEach(unit => {
            if (value.includes(unit)) {
                const numericValue = parseFloat(value.replace(unit, ''));
                result = [numericValue, unit];
            }
        });

        return result || [];
    }

    // Additional methods can be added as per requirements.
}

// Usage example:
const animationHelper = new AnimationHelper(
    function(normalizeFnArgs: any[], arg2?: any) {
        return { mode: "default" };
    },
    function(option: any) {
        return true; // Or actual condition logic
    }
);

animationHelper.hide({});  // Example usage
animationHelper.toggle(true);  // Another example usage