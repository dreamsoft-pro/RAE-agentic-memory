/**
 * Service: slider
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';

interface Slide {
  url: string;
  link: string;
}

interface SliderProps {
  slides: Slide[];
}

const Slider: React.FC<SliderProps> = ({ slides }) => {
  return (
    <div id="slider">
      <div className="container-fluid slider-original no-padding">
        <div className="row-fluid">
          <div className="col-xs-12 no-padding">
            <div className="content-header-carousel">
              <Carousel autoPlay infiniteLoop showThumbs={false} showStatus={false}>
                {slides.map((image, index) => (
                  <div key={index}>
                    <a href={image.link} target="_blank" rel="noopener noreferrer">
                      <span style={{ background: `url(${image.url}) no-repeat top center` }} />
                    </a>
                  </div>
                ))}
              </Carousel>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Slider;