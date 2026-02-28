/**
 * Service: galleries-simple
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import Gallery from 'react-photo-gallery';

interface GalleryItem {
  url: string;
  // Add other properties as needed
}

interface GalleryData {
  langs: { [key: string]: { name: string } };
  items: GalleryItem[];
  order: number;
}

const GalleriesSimple = () => {
  const [galleries, setGalleries] = useState<GalleryData[]>([]);
  const [currentLang, setCurrentLang] = useState({ code: '' });

  useEffect(() => {
    axios.get('/api/galleries').then(response => {
      setGalleries(response.data);
    });
  }, []);

  const hasFormats = (gallery: GalleryData) => gallery.items.length > 0;

  return (
    <div className="row">
      {galleries.length > 0 && galleries
        .filter(hasFormats)
        .map((gallery, index) => (
          <div className="col-xs-12" key={index}>
            <h3>{gallery.langs[currentLang.code].name}</h3>
            <Gallery photos={gallery.items} />
          </div>
        ))}
    </div>
  );
};

export default GalleriesSimple;