/**
 * Service: galleries
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
  // Add other properties if needed
}

interface GalleryData {
  langs: { [key: string]: { name: string } };
  items: GalleryItem[];
  order: number;
}

const Galleries = () => {
  const [galleries, setGalleries] = useState<GalleryData[]>([]);
  const [currentLang, setCurrentLang] = useState({ code: 'en' }); // Adjust based on your language setup

  useEffect(() => {
    axios.get('/api/galleries').then(response => {
      setGalleries(response.data);
    });
  }, []);

  const hasFormats = (gallery: GalleryData) => gallery.items.length > 0;

  return (
    <div>
      {galleries
        .filter(hasFormats)
        .sort((a, b) => a.order - b.order)
        .map((gallery, index) => (
          <div key={index} className="panel panel-default">
            <div className="panel-heading">
              <h3 className="panel-title">{gallery.langs[currentLang.code].name}</h3>
            </div>
            <div className="panel-body">
              <Gallery photos={gallery.items} />
            </div>
          </div>
        ))}
    </div>
  );
};

export default Galleries;