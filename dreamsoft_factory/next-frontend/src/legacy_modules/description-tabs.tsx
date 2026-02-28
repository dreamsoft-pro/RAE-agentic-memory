/**
 * Service: description-tabs
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Thumbnail {
  files: { url: string }[];
}

interface Description {
  langs: { [key: string]: { name: string; description: string } };
  showLess?: boolean;
}

interface Gallery {
  items: any[];
  langs: { [key: string]: { name: string } };
}

interface Props {
  thumbnails: Thumbnail[];
  descriptions: Description[];
  galleries: Gallery[];
  patterns: any[];
  currentLang: { code: string };
}

const ModernizedComponent: React.FC<Props> = ({ thumbnails, descriptions, galleries, patterns, currentLang }) => {
  const [activeTab, setActiveTab] = React.useState(0);

  return (
    <div className="row">
      <div className="col-md-2">
        {thumbnails
          .filter(thumbnail => thumbnail.files.length > 0)
          .map((thumbnail, index) => (
            <div key={index} className="center-block thumbnail-margin">
              {thumbnail.files.map((file, fileIndex) => (
                <a
                  key={fileIndex}
                  href="#"
                  data-target="#showThumbnail"
                  data-toggle="modal"
                  onClick={() => zoomStaticImage(file.url)}
                >
                  <img loading="lazy" src={file.url} className="img-responsive" />
                </a>
              ))}
            </div>
          ))}
      </div>
      <div className="col-md-10">
        <div className="panel with-nav-tabs">
          <div className="panel-heading">
            <ul className="nav nav-tabs">
              {descriptions
                .filter(description => description.langs[currentLang.code].name)
                .map((description, index) => (
                  <li key={index}>
                    <a
                      href="#"
                      data-target={`#description-tab-${index}`}
                      data-toggle="tab"
                    >
                      {description.langs[currentLang.code].name}
                    </a>
                  </li>
                ))}
              {galleries
                .filter(gallery => gallery.items.length > 0)
                .map((gallery, index) => (
                  <li key={index}>
                    <a
                      href="#"
                      data-target={`#gallery-tab-${index}`}
                      data-toggle="tab"
                    >
                      {gallery.langs[currentLang.code].name}
                    </a>
                  </li>
                ))}
              {patterns.length > 0 && (
                <li>
                  <a href="#" data-target="#patterns-tab" data-toggle="tab">
                    {'models' | translate}
                  </a>
                </li>
              )}
            </ul>
          </div>
          <div className="panel-body">
            <div className="tab-content">
              {descriptions.map((description, index) => (
                <div key={index} className="tab-pane" id={`description-tab-${index}`}>
                  {description.showLess ? (
                    <>
                      <div hidden={!description.initHide}>{description.langs[currentLang.code].description}</div>
                      <div hidden={description.initHide}>{description.langs[currentLang.code].description}</div>
                      <div className="pull-right">
                        <button onClick={() => (description.initHide ? description.initHide : true)}>
                          {description.initHide ? 'expand' | translate : 'collapse' | translate}
                        </button>
                      </div>
                    </>
                  ) : (
                    <div>{description.langs[currentLang.code].description}</div>
                  )}
                </div>
              ))}
              {galleries.map((gallery, index) => (
                <div key={index} className="tab-pane" id={`gallery-tab-${index}`}>
                  <ng-gallery images={gallery.items} thumbs-num={gallery.items.length} />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModernizedComponent;