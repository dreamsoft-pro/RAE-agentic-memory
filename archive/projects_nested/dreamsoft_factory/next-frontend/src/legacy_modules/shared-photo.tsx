/**
 * Service: shared-photo
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const SharedPhoto = ({ photo, selectPhoto, actualPhoto }) => {
    return (
        <div className="container" id="content-shared-folder">
            <div className="row">
                <div className="col-md-12">
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            <h2 className="panel-title">{'picture' | translate} - {photo.name}</h2>
                        </div>
                        <div className="panel-body">
                            <div className="row">
                                <div className="col-md-12">
                                    <ul className="nav nav-tabs">
                                        <li className="pull-left"></li>
                                        <li className="pull-right"></li>
                                    </ul>
                                </div>
                            </div>
                            <div className="roundborder margintop" ng-show="photo">
                                <div className="panel" id="panel-product-menu">
                                    {/* Content for the panel */}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="myModal" className="modal fade" tabIndex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                        <div className="modal-dialog">
                            <div className="modal-content">
                                <div className="modal-body modalImage">
                                    <img loading="lazy" src={actualPhoto.imageUrl} alt="photo" className="img-responsive" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="panel-heading">
                <div className="row">
                    <div className="myPhotos">
                        <div tabIndex={photo.index} className="col-md-3 col-xs-6">
                            <div className="boxPhoto">
                                <img loading="lazy" data-toggle={photo.imageUrl.length > 0 ? 'modal' : ''} data-target={photo.imageUrl.length > 0 ? '#myModal' : ''} onClick={() => selectPhoto(photo)} src={photo.minUrl} className="img-responsive myPhoto" alt={photo.name} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SharedPhoto;