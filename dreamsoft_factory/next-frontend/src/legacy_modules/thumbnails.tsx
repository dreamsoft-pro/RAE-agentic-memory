/**
 * Service: thumbnails
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Thumbnail {
  langs: { [key: string]: { name: string } };
  files: { url: string }[];
}

interface Props {
  thumbnails: Thumbnail[];
  currentLang: { code: string };
}

const Thumbnails: React.FC<Props> = ({ thumbnails, currentLang }) => {
  return (
    <div className="panel panel-default" id="panel-product-thumbnails">
      {thumbnails
        .filter(thumbnail => thumbnail.files.length > 0)
        .sort((a, b) => a.order - b.order)
        .map((thumbnail, index) => (
          <div className="panel panel-default" key={index}>
            <div className="panel-heading">
              <h3 className="panel-title">{thumbnail.langs[currentLang.code].name}</h3>
            </div>
            <div className="panel-body">
              {thumbnail.files.map((file, fileIndex) => (
                <img loading="lazy" key={fileIndex} src={file.url} alt="" className="img-responsive" />
              ))}
            </div>
          </div>
        ))}
    </div>
  );
};

export default Thumbnails;