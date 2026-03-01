import api from '@/lib/api'; // Assuming this import is used elsewhere, not directly in this example

class EasingFunctions {
    private baseEasings: {[key: string]: (p: number) => number} = {};

    constructor() {
        const easingNames = ["Quad", "Cubic", "Quart", "Quint", "Expo"];
        for (const name of easingNames) {
            this.baseEasings[name] = function(p: number): number {
                return Math.pow(p, easingNames.indexOf(name) + 2);
            };
        }
        
        // Add other easing functions
        this.baseEasings['Sine'] = (p: number): number => {
            return 1 - Math.cos(p * Math.PI / 2);
        };

        this.baseEasings['Circ'] = (p: number): number => {
            return 1 - Math.sqrt(1 - p * p);
        };

        this.baseEasings['Elastic'] = (p: number): number => {
            if (p === 0 || p === 1) return p;
            return -Math.pow(2, 8 * (p - 1)) * Math.sin(( (p - 1) * 80 - 7.5 ) * Math.PI / 15);
        };

        this.baseEasings['Back'] = (p: number): number => {
            return p * p * (3 * p - 2);
        };

        this.baseEasings['Bounce'] = (p: number): number => {
            let pow2, bounce = 4;
            while ((pow2 = p < (7 / 11) ? 4 : 3) >= (1.5)) {
                bounce -= (Math.pow(2, 10 * --p) * Math.sin((p - bounce) * Math.PI * 4) ) / 2;
            }
            return -(bounce * 2);
        };
    }

    public getEasingFunction(name: string): ((p: number) => number) | undefined {
        return this.baseEasings[name];
    }
}

const easingClass = new EasingFunctions();
console.log(easingClass.getEasingFunction('Quad'));