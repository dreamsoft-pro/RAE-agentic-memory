/**
 * Service: PhotoGalleryManager
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import { GoogleMap, Marker, useJsApiLoader } from '@react-google-maps/api';
import { toast } from 'react-toastify';

/**
 */
export const PhotoGalleryManager: React.FC = () => {
    const [photos, setPhotos] = useState<any[]>([]);
    const [actualPhoto, setActualPhoto] = useState<any>(null);
    const [isSliderOn, setIsSliderOn] = useState(false);
    const [brightness, setBrightness] = useState(0);
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // Load initial folder data
    useEffect(() => {
        loadPhotos();
    }, []);

    const loadPhotos = async () => {
        try {
            const response = await axios.get('/api/photos/my-gallery');
            setPhotos(response.data);
        } catch (error) {
            toast.error("Nie udało się załadować zdjęć");
        }
    };

    /**
     */
    const applyFilters = useCallback(() => {
        const canvas = canvasRef.current;
        if (!canvas || !actualPhoto) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Apply brightness and other effects using CSS-like filters or manual matrix
        ctx.filter = `brightness(${100 + brightness}%)`;
        const img = new Image();
        img.src = actualPhoto.url;
        img.onload = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
        };
    }, [actualPhoto, brightness]);

    /**
     */
    const handleRemoveTag = async (photoId: string, tag: string) => {
        try {
            await axios.delete(`/api/photos/${photoId}/tags/${tag}`);
            setPhotos(prev => prev.map(p => 
                p._id === photoId ? { ...p, tags: p.tags.filter((t: string) => t !== tag) } : p
            ));
        } catch (error) {
            console.error("Tag removal failed");
        }
    };

    return (
        <div className="flex flex-col space-y-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {photos.map(photo => (
                    <div 
                        key={photo._id} 
                        className="cursor-pointer hover:opacity-80 transition"
                        onClick={() => setActualPhoto(photo)}
                    >
                        <img src={photo.thumbnail} alt={photo.name} className="rounded-lg shadow-sm" />
                    </div>
                ))}
            </div>

            {actualPhoto && (
                <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
                    <h2 className="text-xl font-bold mb-4">Edycja: {actualPhoto.name}</h2>
                    <canvas 
                        ref={canvasRef} 
                        width={800} 
                        height={600} 
                        className="w-full max-w-2xl bg-gray-50 rounded border"
                    />
                    
                    <div className="mt-4 flex items-center space-x-4">
                        <label>Jasność:</label>
                        <input 
                            type="range" 
                            min="-100" 
                            max="100" 
                            value={brightness}
                            onChange={(e) => setBrightness(parseInt(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-teal-600"
                        />
                    </div>
                </div>
            )}
        </div>
    );
};

export default PhotoGalleryManager;
