import { FC } from 'react';
import api from '@/lib/api'; // Assuming this import is necessary for some logic not shown here

interface MyComponentProps {
    noPropagation?: boolean;
}

class MyComponentClass {
    currentContainer: any; // Define your type based on actual implementation
    delayedTriggers: Function[] = []; // Array of functions to be executed

    _trigger(event: string, eventObj: Event, uiHash: Record<string, any>) {
        console.log(`Triggering ${event} with UI Hash`, uiHash);
        // Implement your trigger logic here
    }

    _uiHash(thisArg?: any): Record<string, any> {
        return { /* Your hash generation logic */ };
    }

    checkContainerChange(noPropagation: boolean = false) {
        if (this !== this.currentContainer) {
            if (!noPropagation) {
                const self = this; // Store the context to avoid issues with 'this'
                
                this.delayedTriggers.push(function(event) { self._trigger("remove", event, self._uiHash()); });
                this.delayedTriggers.push((function(c) { return function(event) { c._trigger("receive", event, self._uiHash(self)); }; })(this.currentContainer));
                this.delayedTriggers.push((function(c) { return function(event) { c._trigger("update", event, self._uiHash(self)); }; })(this.currentContainer));
            }
        }
    }

    // Example usage
    componentDidMount() {
        const noPropagation = false; // Set based on your requirements
        this.checkContainerChange(noPropagation);
    }
}

// If you need a React Component wrapper
const MyComponent: FC<MyComponentProps> = (props) => {
    return <div></div>; // Your component JSX
};

export default MyComponent;