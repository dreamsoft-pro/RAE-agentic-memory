import { useEffect } from 'react';
import api from '@/lib/api';

interface SortableItem {
  direction: string;
  item?: HTMLElement | null; // Assuming `item` is an optional property to handle edge cases.
}

class SortableClass {
  placeholder!: HTMLElement; // Placeholder element, assuming it's initialized elsewhere in the class
  counter = 0; // Counter variable

  _rearrange(event: Event, i: SortableItem, a?: HTMLElement[], hardRefresh?: boolean): void {
    if (a) {
      a[0].appendChild(this.placeholder);
    } else {
      i.item?.parentNode!.insertBefore(this.placeholder, this.direction === "down" ? i.item : i.item.nextSibling);
    }

    // Performance optimization using setTimeout and counter
    const counter = ++this.counter;

    useEffect(() => {
      if (counter === this.counter) {
        this.refreshPositions(!hardRefresh); // Precompute after each DOM insertion, NOT on mousemove
      }
    }, []);
  }

  private _delay(callback: () => void): void {
    setTimeout(callback, 0);
  }

  refreshPositions(hardRefresh?: boolean): Promise<void> {
    return new Promise((resolve) => {
      api.get('/some-endpoint') // Replace with actual API call
        .then(response => {
          console.log('Response received:', response.data);
          resolve();
        })
        .catch(error => {
          console.error('Error during refreshPositions:', error);
          resolve(); // Resolve even on failure to avoid blocking indefinitely
        });
    });
  }

  _clear(event: Event, noPropagation?: boolean): void {
    // Placeholder for clearing logic. Implementation depends on requirements.
  }
}

export default SortableClass;