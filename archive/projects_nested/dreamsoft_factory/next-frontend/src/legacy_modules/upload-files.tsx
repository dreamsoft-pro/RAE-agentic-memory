/**
 * Service: upload-files
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const UploadFilesModal: React.FC = () => {
    return (
        <div className="modal-header">
            <h3 className="modal-title">{'upload_files' | translate}: </h3>
            <div className="upload-file-info">
                <div ngStaticContents className="staticContentBox" content={files.uploadInfo} />
            </div>
        </div>
        <div className="modal-body">
            {/*thumbnails for images*/}
            <style jsx>{`
                .my-drop-zone {
                    border: dotted 3px lightgray;
                }
                .nv-file-over {
                    border: dotted 3px red;
                }
                /* Default class applied to drop zones on over */
                .another-file-over-class {
                    border: dotted 3px green;
                }
                canvas {
                    background-color: #f3f3f3;
                    -webkit-box-shadow: 3px 3px 3px 0 #e3e3e3;
                    -moz-box-shadow: 3px 3px 3px 0 #e3e3e3;
                    box-shadow: 3px 3px 3px 0 #e3e3e3;
                    border: 1px solid #c3c3c3;
                    height: 100px;
                    margin: 6px 0 0 6px;
                }
                .fileinput-button input {
                    position: absolute;
                    top: 0;
                    right: 0;
                    margin: 0;
                    opacity: 0;
                    -ms-filter: 'alpha(opacity=0)';
                    font-size: 200px !important;
                    direction: ltr;
                    cursor: pointer;
                }
                input[type=file] {
                    display: block;
                }
            `}</style>
            <button ngClick="uploader.uploadAll()" ngDisabled={!uploader.getNotUploadedItems().length}>
                <span className="fa fa-upload"></span>
                {'upload_all' | translate}
            </button>
            <button type="button" className="btn btn-warning btn-s" ngClick="uploader.cancelAll()" ngDisabled={!uploader.isUploading}>
                <span className="fa fa-ban"></span>
                {'cancel_all '| translate}
            </button>
            <button type="button" className="btn btn-danger btn-s" ngClick="uploader.clearQueue()" ngDisabled={!uploader.queue.length}>
                <span className="fa fa-trash"></span>
                {'remove_all' | translate}
            </button>
            <button type="button" className="btn btn-danger btn-s pull-right" ngClick="cancel()">
                <span className="fa fa-remove"></span>
                {'close' | translate}
            </button>
        </div>
        <div className="row">
            <div className="col-md-12">
                <div ngShow="uploader.isHTML5">
                    <div nvFileDrop="" uploader={uploader}>
                        <div nvFileOver="" uploader={uploader} overClass="another-file-over-class" className="well my-drop-zone">
                            {'drop_files_here' | translate}
                        </div>
                    </div>
                </div>
                <span className="btn btn-success fileinput-button">
                    <i className="fa fa-plus"></i>
                    <span>{'add_files' | translate}...</span>
                    <input type="file" nvFileSelect="" uploader={uploader} multiple />
                </span>
                <p className="pull-right">{'number_of_files' | translate}: {uploader.queue.length}</p>
            </div>
            <hr />
            <div className="col-md-12">
                <div className="row">
                    <div className="col-md-12 ng-binding">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th className="col-md-3">{'name' | translate}</th>
                                    <th className="col-md-2" ngShow="uploader.isHTML5">{'size' | translate}</th>
                                    <th className="col-md-2" ngShow="uploader.isHTML5">{'progress' | translate}</th>
                                    <th className="col-md-2">{'status' | translate}</th>
                                    <th className="col-md-2">{'actions' | translate}</th>
                                </tr>
                            </thead>
                            <tbody>
                                {uploader.queue.map((item, index) => (
                                    <tr key={index}>
                                        <td className="col-md-3">
                                            <strong tooltip={item.file.name}>{item.file.name | limitTo: 10}{item.file.name.length > 10 ? '...' : ''}</strong>
                                            <div ngShow="uploader.isHTML5" ngThumb={{ file: item._file, height: 100 }}></div>
                                            <div ngThumb={{ file: item.file, width: 100, height: 100 }}></div>
                                        </td>
                                        <td className="col-md-2" ngShow="uploader.isHTML5" nowrap>{item.file.size / 1024 / 1024 | number: 2} MB</td>
                                        <td className="col-md-2" ngShow="uploader.isHTML5">
                                            <div className="progress" style={{ marginBottom: 0 }}>
                                                <div className="progress-bar" role="progressbar" style={{ width: `${item.progress}%` }}></div>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UploadFilesModal;