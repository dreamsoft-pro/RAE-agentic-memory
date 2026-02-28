import api from '@/lib/api';

class DragManager {
  originalPosition: boolean | null = null; // Initialize as null to ensure it's defined before use.
  containment?: [number, number, number, number]; // Array type for the containment boundary.
  offset: { click: { left: number; top: number } };

  constructor(offset: { click: { left: number; top: number } }) {
    this.offset = offset;
  }

  handleDragEvent(event: MouseEvent): void {
    if (this.originalPosition) {
      const { containment, offset } = this;

      if (containment && event.pageX - offset.click.left < containment[0]) {
        event.pageX = containment[0] + offset.click.left;
      }
      if (containment && event.pageY - offset.click.top < containment[1]) {
        event.pageY = containment[1] + offset.click.top;
      }
      if (containment && event.pageX - offset.click.left > containment[2]) {
        event.pageX = containment[2] + offset.click.left;
      }
      if (containment && event.pageY - offset.click.top > containment[3]) {
        event.pageY = containment[3] + offset.click.top;
      }

      // If you need to do something with the adjusted pageX and pageY, implement it here.
    }
  }
}