/**
 * Service: photo-facebook
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

interface PhotoModalProps {
  photo: any;
  domainHost: string;
  currentLang: { code: string };
}

const PhotoModal: React.FC<PhotoModalProps> = ({ photo, domainHost, currentLang }) => {
  const { t } = useTranslation();

  return (
    <div className="modal-header">
      <h4 className="modal-title">{t('share')} - {photo.name}</h4>
    </div>
    <div className="modal-body editPhotoModal">
      <div className="row">
        <div className="col-md-12">
          <div id="fb-root"></div>
          <script>(function(d, s, id) {
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) return;
            js = d.createElement(s); js.id = id;
            js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1";
            fjs.parentNode.insertBefore(js, fjs);
          })(document, 'script', 'facebook-jssdk');</script>

          <div className="fb-share-button" data-href={`http://${domainHost}/${currentLang.code}/udostepnione-zdjecie/${photo._id}`}
               data-layout="box_count" data-size="small" data-mobile-iframe="true">
            <a href={`https://www.facebook.com/sharer/sharer.php?u=http://${domainHost}/${currentLang.code}/udostepnione-zdjecie/${photo._id}/facebook&src=sdkpreparse`}
               className="fb-xfbml-parse-ignore" target="_blank">
              {t('share_on_facebook')}
            </a>
          </div>
        </div>
      </div>
    </div>
    <div className="modal-footer">
      <button className="btn btn-default" onClick={() => console.log('close')}>{t('close')}</button>
    </div>
  );
};

export default PhotoModal;