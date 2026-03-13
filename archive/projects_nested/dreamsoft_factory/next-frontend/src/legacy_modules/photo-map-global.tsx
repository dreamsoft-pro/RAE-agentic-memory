/**
 * Service: photo-map-global
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface PhotoMapGlobalProps {
  actualPhoto: any;
  nextExist: (photo: any) => boolean;
  previousExist: (photo: any) => boolean;
  nextPhoto: (photo: any) => void;
  previousPhoto: (photo: any) => void;
  closeModal: () => void;
}

const PhotoMapGlobal: React.FC<PhotoMapGlobalProps> = ({
  actualPhoto,
  nextExist,
  previousExist,
  nextPhoto,
  previousPhoto,
  closeModal,
}) => {
  return (
    <div className="modal-body editPhotoModal">
      <div className="row">
        <div className="col-xs-10 col-xs-offset-1">
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-body modalImage">
                <img loading="lazy" src={actualPhoto.imageUrl} alt="photo" className="img-responsive"/>
                {nextExist(actualPhoto) && (
                  <button className="btn btn-info nextButton" onClick={() => nextPhoto(actualPhoto)}>
                    <i className="fa fa-arrow-right" aria-hidden="true"></i>
                  </button>
                )}
                {previousExist(actualPhoto) && (
                  <button className="btn btn-info previousButton" onClick={() => previousPhoto(actualPhoto)}>
                    <i className="fa fa-arrow-left" aria-hidden="true"></i>
                  </button>
                )}
                <button className="btn btn-danger closeButton" onClick={closeModal}>
                  <i className="fa fa-times" aria-hidden="true"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="modal-footer">
        <button className="btn btn-default" onClick={() => {}}>{'close' /* Assuming translate is handled elsewhere */}</button>
      </div>
    </div>
  );
};

export default PhotoMapGlobal;