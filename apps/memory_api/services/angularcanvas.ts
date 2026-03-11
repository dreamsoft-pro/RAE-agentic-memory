javascript
import { CanvasService } from '@/lib/api';

function rotate() {}

export default function link(scope, element, attrs) {
    const ticker = createjs.Ticker.addEventListener("tick", handleTick);

    const photo = scope.photo;
    const canvas = element[0];
    console.log('photo', photo);
    
    canvas.width = photo.width;
    canvas.height = photo.height;

    const context = canvas.getContext('2d');
    const stage = new createjs.Stage(canvas);
    const container = new createjs.Container();

    const image = new Image();
    image.crossOrigin = "Anonymous";
    image.src = photo.minUrl;

    image.onload = function() {
        const bitmap = new createjs.Bitmap(image);
        const scale = canvas.width / photo.width;
        
        bitmap.scaleX = bitmap.scaleY = scale;
        container.addChild(bitmap);
        stage.addChild(container);
    };
}

function handleTick(event) {
    createjs.Ticker.setFPS(60);
    createjs.Ticker.addEventListener("tick", stage);
}
