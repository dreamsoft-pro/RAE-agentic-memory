/**
 * Service: photo-share
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

interface PhotoShareProps {
  photo: {
    emailShared: boolean;
    sharedEmails: string[];
  };
  onSave: (email: string) => void;
  onClose: () => void;
}

const PhotoShare: React.FC<PhotoShareProps> = ({ photo, onSave, onClose }) => {
  const { t } = useTranslation();

  return (
    <div className="modal-header">
      <h4 className="modal-title">{t('share_with_email')}</h4>
    </div>
    <div className="modal-body editPhotoModal">
      <div className="row">
        {photo.emailShared && (
          <>
            <h4>{t('shered_for')}:</h4>
            {photo.sharedEmails.map((email, index) => (
              <div key={index} tabIndex={index} className="col-md-3 col-xs-6 repeatContainer">
                <div>{email}</div>
              </div>
            ))}
          </>
        )}
        <div className="col-md-12">
          <form onSubmit={(e) => { e.preventDefault(); onSave(email); }}>
            <div className="form-body">
              <div className="form-group">
                <div className="col-xs-12">
                  <label htmlFor="sharedEmail">{t('email')}</label>
                  <input id="sharedEmail" className="form-control" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
              </div>
              <div className="form-group">
                <div className="col-md-3 col-md-offset-9">
                  <button type="submit" className="btn btn-success btn-block btn-submit">{t('save')}</button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div className="modal-footer">
      <button className="btn btn-default" onClick={onClose}>{t('close')}</button>
    </div>
  );
};

export default PhotoShare;