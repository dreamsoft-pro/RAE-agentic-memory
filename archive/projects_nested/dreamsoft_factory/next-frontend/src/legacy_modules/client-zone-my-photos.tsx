/**
 * Service: client-zone-my-photos
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';
import Paging from './Paging'; // Assuming you have a custom paging component

const MyPhotos = ({ photos, sort, pagingSettings, getNextPage, selectPhoto }) => {
    const { t } = useTranslation();

    return (
        <div>
            <div className="row">
                <div className="col-md-12 text-center">
                    <button type="button" className="btn btn-lg btn-info" onClick={() => /* navigate to folders */}>
                        <i className="fa fa-folder-open-o" aria-hidden="true"></i> {t('back')}
                    </button>
                </div>
            </div>
            <div className="row">
                <div className="col-md-12 text-center">
                    <div>
                        <Paging 
                            page={pagingSettings.currentPage} 
                            pageSize={pagingSettings.pageSize} 
                            total={pagingSettings.total} 
                            onNext={(page) => getNextPage(page)} 
                            showPrevNext={true} 
                            showFirstLast={true} 
                            hideIfEmpty={true} 
                        />
                    </div>
                </div>
            </div>
            <div className="row roundborder margintop">
                {photos.map(photo => (
                    <div key={photo._id} className="col-md-3">
                        <img 
                            onClick={() => selectPhoto(photo)} 
                            src={photo.thumbnail || 'placeholder'} 
                            alt={photo.name} 
                            className="img-responsive myPhoto" 
                        />
                        <div className="toolBoxBottom bg-basic">
                            <button type="button" className="btn btn-sm btn-success dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <i className="fa fa-pencil-square-o" aria-hidden="true"></i>
                            </button>
                            <ul className="dropdown-menu">
                                <li><a onClick={() => movePhoto(folder, photo)}><i className="fa fa-arrows-v" aria-hidden="true"></i> {t('move')}</a></li>
                                <li><a onClick={() => copyPhoto(folder, photo)}><i className="fa fa-clone" aria-hidden="true"></i> {t('copy')}</a></li>
                            </ul>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default MyPhotos;