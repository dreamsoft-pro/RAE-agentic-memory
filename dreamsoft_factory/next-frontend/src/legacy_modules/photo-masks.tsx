/**
 * Service: photo-masks
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';
import './photoMasks.css'; // Assuming you have a corresponding CSS file for styling

interface PhotoMaskProps {
  masks: any[];
  currentPage: number;
  numberOfPages: () => number;
  pageSize: number;
  photo: string;
  selectMask: (photo: string, mask: any) => void;
  getMaskImage: (photo: string, mask: any) => string;
  setCurrentPage: (page: number) => void;
}

const PhotoMasks: React.FC<PhotoMaskProps> = ({ masks, currentPage, numberOfPages, pageSize, photo, selectMask, getMaskImage, setCurrentPage }) => {
  const { t } = useTranslation();

  return (
    <>
      <div className="modal-header">
        <h4 className="modal-title">{t('masks')}</h4>
      </div>
      <div className="modal-body maskPhotoModal">
        <div className="row">
          <div className="col-md-12">
            <button 
              className="btn btn-primary" 
              disabled={currentPage === 1} 
              onClick={() => setCurrentPage(currentPage - 1)}
            >
              <i className="fa fa-arrow-left" aria-hidden="true"></i>
            </button>
            {currentPage}/{numberOfPages()}
            <button 
              className="btn btn-primary" 
              disabled={currentPage >= masks.length / pageSize} 
              onClick={() => setCurrentPage(currentPage + 1)}
            >
              <i className="fa fa-arrow-right" aria-hidden="true"></i>
            </button>
            <div className="row row-margin-top">
              {masks[currentPage]?.slice(0, pageSize).map((mask: any, index: number) => (
                <div key={index} className="col-md-3 col-xs-6">
                  <a 
                    onClick={() => selectMask(photo, mask)} 
                    className="thumbnail mask-thumbnail"
                  >
                    <img 
                      loading="lazy" 
                      alt={`maska ${index}`} 
                      src={getMaskImage(photo, mask)} 
                    />
                  </a>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
      <div className="modal-footer">
        <button className="btn btn-default" onClick={() => { /* close logic */ }}>{t('close')}</button>
      </div>
    </>
  );
};

export default PhotoMasks;