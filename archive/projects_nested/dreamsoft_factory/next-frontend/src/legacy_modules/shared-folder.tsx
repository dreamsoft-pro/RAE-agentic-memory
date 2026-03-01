/**
 * Service: shared-folder
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { Translate } from 'react-jhipster'; // Assuming you have a translation function or library

interface Photo {
  imageUrl: string;
  thumbnail: string;
  name: string;
  averageRate: number;
  _id: string;
}

interface Props {
  folder: {
    folderName: string;
    description: string;
    averageRate: number;
    _id: string;
  };
  photos: Photo[];
  rating: {
    max: number;
  };
  pagingSettings: {
    currentPage: number;
    pageSize: number;
    total: number;
  };
  changeLimit: (limit: number) => void;
  getNextPage: (page: number) => void;
}

const SharedFolderComponent: React.FC<Props> = ({ folder, photos, rating, pagingSettings, changeLimit, getNextPage }) => {
  return (
    <div className="container" id="content-shared-folder">
      <div className="row">
        <div className="col-md-12">
          <form>
            <div className="form-body">
              <div className="form-group">
                <div className="col-md-6 col-md-offset-3">
                  <label htmlFor="folderPassword"><Translate contentKey="password" /></label>
                  <input id="folderPassword" type="text" className="form-control" ngModel />
                </div>
              </div>
              <div className="form-group">
                <div className="col-md-6 col-md-offset-3">
                  <button className="btn btn-success btn-block btn-submit"><Translate contentKey="send" /></button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12 text-center">
          <paging page={pagingSettings.currentPage} pageSize={pagingSettings.pageSize} total={pagingSettings.total} pagingAction={getNextPage} showPrevNext={true} showFirstLast={true} hideIfEmpty={true} ulClass="pagination" />
        </div>
      </div>
      {photos.length > 0 && (
        <div className="roundborder margintop">
          <div className="panel">
            <div className="panel-body">
              <div className="row">
                <div className="myPhotos">
                  {photos.map((photo, index) => (
                    <div key={index} className="col-md-3 col-xs-6 repeatContainer" tabIndex={index}>
                      <div className="boxPhoto">
                        <img loading="lazy" data-toggle={photo.imageUrl.length > 0 ? 'modal' : ''} data-target={photo.imageUrl.length > 0 ? '#myModal' : ''} onClick={() => selectPhoto(photo)} src={photo.thumbnail} className="img-responsive myPhoto" alt={photo.name} />
                      </div>
                      <div className="toolBoxBottom bg-basic">
                        <div ngStarRating itemId={photo._id} type="photo" ratingValue={photo.averageRate} max={rating.max} onRatingSelected={(selected) => getSelectedRating({ selected })} />
                        <b>{photo.averageRate}/{rating.max}</b>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      <div className="panel panel-default">
        <div className="panel-heading">
          <h2 className="panel-title"><Translate contentKey="my_folder" values={{ folderName: folder.folderName }} /></h2>
        </div>
        <div className="panel-body">
          <div className="row">
            <div className="col-md-12">
              {folder.description && <div className="well well-sm">{folder.description}</div>}
            </div>
          </div>
          <div className="row">
            <div className="col-md-12">
              <ul className="nav nav-tabs">
                <li className="pull-left">
                  {folder._id && (
                    <>
                      <Translate contentKey="rate_folder" values={{ averageRate: folder.averageRate, max: rating.max }} />
                      <div ngStarRating itemId={folder._id} type="folder" ratingValue={folder.averageRate} max={rating.max} onRatingSelected={(selected) => getSelectedRating({ selected })} />
                    </>
                  )}
                </li>
                <li className="dropdown pull-right">
                  <a data-toggle="dropdown" className="dropdown-toggle" href="#"><i className="fa fa-list-ol"></i><span className="caret"></span></a>
                  <ul className="dropdown-menu">
                    {pageSizeSelect.map((limit, index) => (
                      <li key={index}><a className="fa33" onClick={() => changeLimit(limit)}>{limit}</a></li>
                    ))}
                  </ul>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SharedFolderComponent;