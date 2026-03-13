/**
 * Service: project-facebook
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

interface ProjectShareModalProps {
    project: {
        projectName: string;
        _id: string;
    };
    domainHost: string;
    currentLang: {
        code: string;
    };
}

const ProjectShareModal: React.FC<ProjectShareModalProps> = ({ project, domainHost, currentLang }) => {
    const { t } = useTranslation();

    return (
        <div className="modal-header">
            <h4 className="modal-title">
                {t('share')} - {project.projectName}
            </h4>
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
                    }(document, 'script', 'facebook-jssdk'));</script>

                    <div className="fb-share-button" data-href={`https://${domainHost}/en/${currentLang.code}/udostepniony-projekt/${project._id}/facebook`}
                        data-layout="box_count" data-size="small" data-mobile-iframe="true">
                        <a className="fb-xfbml-parse-ignore" target="_blank" href={`https://www.facebook.com/sharer/sharer.php?u=http://${domainHost}/en/${currentLang.code}/udostepniony-projekt/${project._id}/facebook&src=sdkpreparse`}>
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

export default ProjectShareModal;