/**
 * Service: project-share
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

const ProjectShareModal: React.FC = () => {
    const { t } = useTranslation();

    return (
        <div className="modal-header">
            <h4 className="modal-title">{t('share_with_email')}</h4>
        </div>
        <div className="modal-body projectShareModal">
            <div className="row">
                <div className="col-md-12">
                    <form className="form-horizontal" role="form" onSubmit={() => {}}>
                        <div className="form-body">
                            <div className="form-group">
                                <div className="col-xs-12">
                                    <label htmlFor="sharedEmail">{t('email')}</label>
                                    <input id="sharedEmail" className="form-control" type="email" />
                                </div>
                            </div>
                            <div className="form-group">
                                <div className="col-md-3 col-md-offset-9">
                                    <button className="btn btn-success btn-block btn-submit">{t('save')}</button>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ProjectShareModal;