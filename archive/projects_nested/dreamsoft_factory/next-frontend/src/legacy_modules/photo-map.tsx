/**
 * Service: photo-map
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

const EditPhotoModal: React.FC = () => {
    const { t, i18n } = useTranslation();

    return (
        <div>
            <div className="modal-header">
                <h4 className="modal-title">{t('edit')}</h4>
            </div>
            <div className="modal-body editPhotoModal">
                <div className="row">
                    <div id="map-asset" style={{ height: '300px' }} className="col-xs-10 col-xs-offset-1">Miejsce na mapke googla</div>
                </div>
                <div className="row row-margin-top">
                    <div className="col-xs-10 col-xs-offset-1">
                        <form className="form-horizontal" role="form" onSubmit={() => {}}>
                            <div className="form-body">
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
                <button type="button" className="btn btn-default" onClick={() => {}}>{t('close')}</button>
            </div>
        </div>
    );
};

export default EditPhotoModal;