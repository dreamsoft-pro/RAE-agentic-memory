/**
 * Service: patterns-thubnails
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Pattern {
  patternFile: string;
  patternIcon: string;
}

interface Thumbnail {
  langs: { [key: string]: { name: string } };
  files: { url: string }[];
}

interface Props {
  patterns: Pattern[];
  thumbnails: Thumbnail[];
  currentType: { names: { [key: string]: string } };
  currentLang: { code: string };
}

const PatternsThumbnails: React.FC<Props> = ({ patterns, thumbnails, currentType, currentLang }) => {
  return (
    <div className="panel panel-default" id="panel-product-patterns-thumbnails">
      <div className="panel-heading">
        <h3 className="panel-title">Szablony</h3>
      </div>
      <div className="panel-body">
        {patterns.length > 0 && (
          <div className="panel-body-patterns clearfix">
            <h4 className="pull-left">{currentType.names[currentLang.code]}</h4>
            <ul className="list-inline pull-right">
              {patterns
                .filter(pattern => pattern.patternFile && pattern.patternIcon)
                .map((pattern, index) => (
                  <li key={index}>
                    <a href={pattern.patternFile} target="_blank" rel="noopener noreferrer">
                      <img loading="lazy" src={pattern.patternIcon} alt="Pattern" />
                    </a>
                  </li>
                ))}
            </ul>
          </div>
        )}
        {thumbnails
          .filter(thumbnail => thumbnail.files.length > 0)
          .map((thumbnail, index) => (
            <div key={index} className="panel-body-thumbnails clearfix">
              <h4>{thumbnail.langs[currentLang.code].name}</h4>
              {thumbnail.files.map((file, fileIndex) => (
                <img loading="lazy" className="img-responsive" key={fileIndex} src={file.url} alt="Thumbnail" />
              ))}
            </div>
          ))}
      </div>
    </div>
  );
};

export default PatternsThumbnails;