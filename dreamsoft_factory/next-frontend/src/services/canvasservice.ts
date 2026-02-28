javascript
import '@/lib/api';

const CanvasService = {};

CanvasService.canvas = null;
CanvasService.context = null;
CanvasService.stage = null;
CanvasService.bitmap = null;

CanvasService.setCanvas = function(newCanvas) {
    this.canvas = newCanvas;
};

CanvasService.getContext = function() {
    return this.context;
};

// [BACKEND_ADVICE] Consider moving complex logic to backend if necessary.
CanvasService.getCanvas = function() {
    return this.canvas;
};

CanvasService.setContext = function(newContext) {
    this.context = newContext;
};

CanvasService.setStage = function(newStage) {
    this.stage = newStage;
};

// [BACKEND_ADVICE] Consider moving complex logic to backend if necessary.
CanvasService.getStage = function() {
    return this.stage;
};

CanvasService.setBitmap = function(newBitamp) {
    this.bitmap = newBitamp;
};
