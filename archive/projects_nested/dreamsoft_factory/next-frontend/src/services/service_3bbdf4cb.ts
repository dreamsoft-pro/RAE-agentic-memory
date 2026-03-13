import api from '@/lib/api';

class MyClass {
    items: any[];
    options: { dropOnEmpty?: boolean };
    currentContainer: any;
    containers: any[];
    direction: string;

    private uiHash(): {[key: string]: any} {
        // This is a placeholder for the actual implementation of _uiHash
        return {};
    }

    private triggerOver(event: Event, containerIndex: number): void {
        const innermostIndex = this.determineInnermostIndex();  // Assuming determineInnermostIndex() exists and returns index.
        
        let cur: number;
        let nearBottom: boolean;
        let dist: number = Infinity; // Initialize distance with infinity
        let itemWithLeastDistance: any;

        for (let j = 0; j < this.items.length; j++) {
            const posProperty = 'top'; // or any other property depending on context
            cur = this.items[j].item.offset()[posProperty];
            nearBottom = false;
            
            if ( event[axis] - cur > this.items[j][sizeProperty] / 2 ) { 
                nearBottom = true; 
            }

            if ( Math.abs(event[axis] - cur) < dist ) {
                dist = Math.abs(event[axis] - cur);
                itemWithLeastDistance = this.items[j];
                this.direction = nearBottom ? "up" : "down";
            }
        }

        if (!itemWithLeastDistance && !this.options.dropOnEmpty) {
            return;
        }

        if (this.currentContainer === this.containers[innermostIndex]) {
            if (!this.currentContainer.containerCache.over) {
                this.containers[innermostIndex]._trigger("over", event, this.uiHash());
                this.currentContainer.containerCache.over = 1;
            }
            return;
        }
    }

    private determineInnermostIndex(): number {
        // Implementation of how to find the innermost index
        return 0; // Placeholder value
    }
}