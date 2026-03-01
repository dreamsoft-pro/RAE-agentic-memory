import api from "@/lib/api";
import { useEffect } from "react";

interface EffectArgs {
    complete?: () => void;
    mode: string;
}

export default class ElementHandler extends React.Component {
    private elem: HTMLElement | null = null; // Initialize the element reference

    constructor(props: {}) {
        super(props);
    }

    private runEffect(next: () => void): void {
        const elem = this.elem as unknown as JQuery<HTMLElement>;
        const { complete, mode } = args;

        function done(): void {
            if (typeof complete === "function") {
                complete.call(elem[0]);
            }
            if (typeof next === "function") {
                next();
            }
        }

        // If the element already has the correct final state
        if ((elem.is(":hidden") && mode === "hide") || (!elem.is(":hidden") && mode === "show")) {
            elem[mode]();
            done();
        } else {
            effectMethod.call(elem[0], args, done);
        }
    }

    private show(option: boolean): void {
        const isStandardAnimation = standardAnimationOption(option);

        if (isStandardAnimation) {
            return this.props.show.apply(this, arguments as any[]);
        } else {
            const args = _normalizeArguments.apply(this, arguments);
            args.mode = "show";
            return this.props.effect.call(this, args);
        }
    }

    componentDidMount(): void {
        // Assuming you set `elem` during mount
        this.elem = document.getElementById("some-element") as HTMLElement;
        if (this.elem) {
            const elemJQuery = $(this.elem); // Convert to jQuery object

            // Example usage of runEffect
            elemJQuery.queue(runEffect.bind(null, () => {})); // Pass a callback for the next effect
        }
    }

    render(): JSX.Element | null {
        return this.props.children;
    }
}