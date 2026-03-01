import api from "@/lib/api";
import { useEffect } from "react";

class MyComponent {
    private offset: any;
    private helperProportions: any;
    private margins: any;
    private helperOffsetParent: any;

    _adjustOffsetFromHelper(obj: string | number[]) {
        if (typeof obj === "string") {
            obj = obj.split(" ");
        }
        if (Array.isArray(obj)) {
            obj = { left: +obj[0], top: +obj[1] || 0 };
        }
        if ("left" in obj) {
            this.offset.click.left = obj.left + this.margins.left;
        }
        if ("right" in obj) {
            this.offset.click.left = this.helperProportions.width - obj.right + this.margins.left;
        }
        if ("top" in obj) {
            this.offset.click.top = obj.top + this.margins.top;
        }
        if ("bottom" in obj) {
            this.offset.click.top = this.helperProportions.height - obj.bottom + this.margins.top;
        }
    }

    _getParentOffset() {
        // Get the offsetParent and cache its position
        this.helperOffsetParent = this.helper?.offsetParent();
        const po = this.helperOffsetParent?.offset();

        if (po) {
            this.offset.parent = po;
        } else {
            console.error("Failed to get parent offset.");
        }
    }

    componentDidMount() {
        // Initialize properties here or in constructor
        this.offset = { click: {} };
        this.helperProportions = {};
        this.margins = {};

        this._getParentOffset();
        this._adjustOffsetFromHelper("10 20"); // Example usage
    }

    render() {
        return <div>My Component</div>;
    }
}

// Usage in a React component (example)
export default function MyNextJSComponent() {
    useEffect(() => {
        const myInstance = new MyComponent();
        myInstance.componentDidMount();
    }, []);

    return (
        <div>
            {/* Your JSX goes here */}
        </div>
    );
}