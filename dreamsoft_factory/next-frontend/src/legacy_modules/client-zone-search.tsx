/**
 * Service: client-zone-search
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const ClientZoneSearch = ({ photos, actualPhoto, nextExist, previousExist, selectPhoto, q }) => {
    return (
        <div>
            <div className="panel panel-default" id="client-zone-my-photos">
                <div className="panel-heading">
                    <h2 className="panel-title">{'search' | translate} - {q}</h2>
                </div>
                <div className="panel-body">
                    <div className="row">
                        <div className="myPhotos">
                            {photos.map((photo, index) => (
                                <div key={photo._id} tabIndex={index} className="col-md-3 col-xs-6 repeatContainer">
                                    <div className="toolBox bg-basic">
                                        <div className="pull-left">
                                            <ul className="rating">
                                                {photo.stars.map((star, starIndex) => (
                                                    <li key={starIndex} className={`star ${star.filled ? 'filled' : ''}`}>
                                                        <i className="fa fa-star" aria-hidden="true"></i>
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>
                                    <div className="boxPhoto">
                                        {photo.EditedUpload ? (
                                            <img loading="lazy" data-toggle={photo.EditedUpload.url.length > 0 ? 'modal' : ''} data-target="#photosModal" onClick={() => selectPhoto(photo)} src={photo.EditedUpload.thumbUrl} className="img-responsive myPhoto" alt={photo.name} />
                                        ) : (
                                            <img loading="lazy" data-toggle={photo.imageUrl.length > 0 ? 'modal' : ''} data-target="#photosModal" onClick={() => selectPhoto(photo)} src={photo.thumbnail} className="img-responsive myPhoto" alt={photo.name} />
                                        )}
                                        <img id={`photo_${photo._id}`} loading="lazy" style={{ display: 'none' }} src={photo.imageUrl} alt="" />
                                    </div>
                                    <div className="toolBox">
                                        <button type="button" className="btn btn-block btn-xs btn-primary" onClick={() => goToFolder(photo)}>{'go_to_folder' | translate}</button>
                                    </div>
                                </div>
                            ))}
                            {photos.length === 0 && (
                                <div className="col-md-offset-1 col-md-10">
                                    <div className="alert alert-info text-center">{'results_is_empty' | translate}</div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            <div id="photosModal" className="modal fade" tabIndex={-1} role="dialog" aria-labelledby="photosModal" aria-hidden="true">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-body modalImage">
                            {actualPhoto.EditedUpload ? (
                                <img loading="lazy" src={actualPhoto.EditedUpload.url} className="img-responsive" />
                            ) : (
                                <img loading="lazy" src={actualPhoto.imageUrl} className="img-responsive" />
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ClientZoneSearch;