import { useEffect } from 'react';
import api from '@/lib/api'; // Assuming this import is necessary for the context

class MyClass {
    private classNameRegex: RegExp;

    constructor() {
        this.classNameRegex = null;
    }

    public removeClass(element: HTMLElement, existClass: string): void {
        if (this.hasClass(element, existClass)) {
            const regExp = new RegExp(`(\\s|^)${existClass}(\\s|$)`);
            element.className = element.className.replace(regExp, ' ');
        }
    }

    private hasClass(element: HTMLElement, className: string): boolean {
        return element.classList.contains(className);
    }
}

export default function MyComponent() {
    useEffect(() => {
        const myClassInstance = new MyClass();

        // Example usage of the class method
        const exampleElement = document.querySelector('.example');
        if (exampleElement) {
            myClassInstance.removeClass(exampleElement, 'example-class');
        }

        return () => {
            // Cleanup logic here if needed
        };
    }, []);

    // Return JSX or other component logic here
    return <div>My Component</div>;
}