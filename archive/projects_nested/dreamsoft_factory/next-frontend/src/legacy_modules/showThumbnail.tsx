/**
 * Service: showThumbnail
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const ShowThumbnail: React.FC = () => {
  const actualFile = []; // Assuming this should be populated with image data

  return (
    <div id="showThumbnail" className="modal" tabIndex={-1} role="dialog" aria-labelledby="showThumbnail" aria-hidden="true">
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-body modalImage">
            <button className="btn btn-danger closeButton" data-dismiss="modal" onClick={() => {}}>
              <i className="fa fa-times" aria-hidden="true"></i>
            </button>
            <div className="image-cover-container">
              {actualFile.map((img, index) => (
                <img key={index} loading="lazy" src={img} alt="" className="center-block img-responsive" />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ShowThumbnail;