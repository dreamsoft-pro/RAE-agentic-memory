import api from '@/lib/api';

class MyComponent extends HTMLElement {
    private containers: any[] = [];
    private placeholder: Node | null = null;
    private options: { helper?: string } = {};
    private dragging: boolean = false;

    // Assuming _uiHash is a method already defined in your class
    private async deactivateContainers() {
        for (let i = this.containers.length - 1; i >= 0; i--) {
            await new Promise<void>((resolve) => {
                this.containers[i]._trigger("deactivate", null, this._uiHash(this));
                if (this.containers[i].containerCache.over) {
                    this.containers[i]._trigger("out", null, this._uiHash(this));
                    this.containers[i].containerCache.over = 0;
                    resolve();
                } else {
                    resolve();
                }
            });
        }

        // Cleanup placeholder and helper if present
        if (this.placeholder && this.placeholder.parentNode) {
            this.placeholder.parentNode.removeChild(this.placeholder);
        }

        if (this.options.helper !== "original" && this.helper?.parentNode) {
            this.helper.parentNode.removeChild(this.helper);
        }

        this.helper = null;
        this.dragging = false;
        this.reverting = false;
        this._noFinalSort = null;
    }
    
    // Assuming you have a method to initialize the component
    private async initComponent() {
        await this.deactivateContainers();
        
        // Additional initialization logic can be added here
    }

    connectedCallback() {
        this.initComponent().then(() => {
            console.log("Initialization complete.");
        }).catch((error) => {
            console.error("Error during initialization:", error);
        });
    }
}

// Define the custom element in your Next.js application entry file or wherever appropriate
customElements.define('my-component', MyComponent);

export default MyComponent;