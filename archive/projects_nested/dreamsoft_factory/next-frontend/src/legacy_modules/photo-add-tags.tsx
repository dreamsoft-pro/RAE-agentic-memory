/**
 * Service: photo-add-tags
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const PhotoAddTags = ({ photo, saveTag, savePerson, saveAuthor, remove, removePlace, removeAuthor, removePerson }) => {
    return (
        <div>
            <div className="modal-header">
                <h4 className="modal-title">{'tags' | translate}</h4>
            </div>
            <div className="modal-body addTags">
                <div className="row">
                    <div className="col-md-10 col-md-offset-1">
                        <ul className="list-inline">
                            {photo.tags.map((tag, index) => (
                                <li key={index}>
                                    {tag}
                                    <button onClick={() => remove(photo, tag)} className="btn btn-xs btn-danger">
                                        <i className="fa fa-times" aria-hidden="true"></i>
                                    </button>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-10 col-md-offset-1">
                        {'place' | translate}: {photo.place}
                        <button onClick={removePlace(photo)} className="btn btn-xs btn-danger">
                            <i className="fa fa-times" aria-hidden="true"></i>
                        </button>
                    </div>
                </div>
                <form onSubmit={savePlace} className="form-horizontal" role="form">
                    <div className="form-body">
                        <div className="form-group">
                            <label htmlFor="place-name" className="col-md-3 control-label">{'place' | translate}</label>
                            <div className="col-md-9">
                                <div className="input-group">
                                    <input type="text" id="place-name" className="form-control" ngModel={place} placeholder={'name' | translate} required />
                                    <span className="input-group-btn">
                                        <button type="submit" className="btn btn-primary btn-search">{'save' | translate}</button>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
                <form onSubmit={saveTag} className="form-horizontal" role="form">
                    <div className="form-body">
                        <div className="form-group">
                            <label htmlFor="tag-name" className="col-md-3 control-label">{'name' | translate}</label>
                            <div className="col-md-9">
                                <div className="input-group">
                                    <input type="text" id="tag-name" className="form-control" ngModel={name} placeholder={'name' | translate} required />
                                    <span className="input-group-btn">
                                        <button type="submit" className="btn btn-primary btn-search">{'save' | translate}</button>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
                <div className="row">
                    <div className="col-md-10 col-md-offset-1">
                        {'author' | translate}: {photo.autor}
                        <button onClick={removeAuthor(photo)} className="btn btn-xs btn-danger">
                            <i className="fa fa-times" aria-hidden="true"></i>
                        </button>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-10 col-md-offset-1">
                        <ul className="list-inline">
                            {photo.peoples.map((person, index) => (
                                <li key={index}>
                                    {person}
                                    <button onClick={() => removePerson(photo, person)} className="btn btn-xs btn-danger">
                                        <i className="fa fa-times" aria-hidden="true"></i>
                                    </button>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
                <form onSubmit={savePerson} className="form-horizontal" role="form">
                    <div className="form-body">
                        <div className="form-group">
                            <label htmlFor="person-name" className="col-md-3 control-label">{'person' | translate}</label>
                            <div className="col-md-9">
                                <div className="input-group">
                                    <input type="text" id="person-name" className="form-control" ngModel={person} placeholder={'person' | translate} required />
                                    <span className="input-group-btn">
                                        <button type="submit" className="btn btn-primary btn-search">{'save' | translate}</button>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
                <form onSubmit={saveAuthor} className="form-horizontal" role="form">
                    <div className="form-body">
                        <div className="form-group">
                            <label htmlFor="author-name" className="col-md-3 control-label">{'author' | translate}</label>
                            <div className="col-md-9">
                                <div className="input-group">
                                    <input type="text" id="author-name" className="form-control" ngModel={author} placeholder={'name' | translate} required />
                                    <span className="input-group-btn">
                                        <button type="submit" className="btn btn-primary btn-search">{'save' | translate}</button>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
            <div className="modal-footer">
                <button onClick={() => $dismiss()} className="btn btn-default">{'close' | translate}</button>
            </div>
        </div>
    );
};

export default PhotoAddTags;