/**
 * Service: angularCanvas
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import createjs from 'createjs';
import CanvasService from './CanvasService'; // Assuming you have a similar service in Next.js/TypeScript

const AngularCanvas: React.FC = ({ photo }) => {
    const canvasRef = React.useRef<HTMLCanvasElement>(null);

    React.useEffect(() => {
        if (canvasRef.current) {
            const canvas = canvasRef.current;
            canvas.width = photo.width;
            canvas.height = photo.height;

            const context = canvas.getContext('2d');
            const stage = new createjs.Stage("photoCanvas");
            const container = new createjs.Container();
            const image = new Image();
            image.crossOrigin = "Anonymous";
            image.src = photo.minUrl;

            image.onload = () => {
                const bitmap = new createjs.Bitmap(image);
                const scale = canvas.width / photo.width;
                bitmap.scaleX = bitmap.scaleY = scale;

                stage.addChild(container);
                container.addChild(bitmap);

                CanvasService.setCanvas(canvas);
                CanvasService.setContext(context);
                CanvasService.setStage(stage);
                CanvasService.setBitmap(bitmap);
                CanvasService.setContainer(container);
            };

            const ticker = createjs.Ticker.addEventListener("tick", handleTick);

            function handleTick(event: any) {
                stage.update();
            }

            return () => {
                ticker.remove();
            };
        }
    }, [photo]);

    return <canvas id="photoCanvas" ref={canvasRef} className="center-block"></canvas>;
};

export default AngularCanvas;