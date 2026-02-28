/**
 * Service: client-zone-my-folders
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { Paging, SortableTable } from '@components/common'; // Assuming these are custom components

interface Folder {
  _id: string;
  folderName: string;
  date: Date;
  description: string;
  imageFiles: Array<any>;
}

interface Props {
  folders: Array<Folder>;
  pagingSettings: {
    currentPage: number;
    pageSize: number;
    total: number;
  };
  addFolder: () => void;
  displayPhotoMap: () => void;
  getNextPage: (page: number) => void;
  changeLimit: (limit: number) => void;
  sortBy: (field: string) => void;
  pageSizeSelect: Array<number>;
}

const ClientZoneMyFolders: React.FC<Props> = ({ folders, pagingSettings, addFolder, displayPhotoMap, getNextPage, changeLimit, sortBy, pageSizeSelect }) => {
  const [sort, setSort] = React.useState({ folderName: 0, date: 0, description: 0 });

  const handleSort = (field: string) => {
    const newSort = { ...sort };
    if (newSort[field] === 1) {
      newSort[field] = -1;
    } else {
      newSort[field] = 1;
    }
    setSort(newSort);
    sortBy(field);
  };

  return (
    <div>
      <div className="roundborder margintop">
        <div className="panel panel-default">
          <div className="panel-heading">
            <h2 className="panel-title">{'my_folders' | translate}</h2>
          </div>
          <div className="panel-body">
            <ul className="nav nav-tabs">
              <li>
                <button type="button" className="btn btn-success" onClick={addFolder}>
                  <span className="fa fa-plus" aria-hidden="true"></span>
                  {'add_folder' | translate}
                </button>
                <button type="button" className="btn btn-success" onClick={displayPhotoMap}>
                  <span className="fa fa-map" aria-hidden="true"></span>
                  {'photo_map' | translate}
                </button>
              </li>
              <li className="dropdown pull-right">
                <a data-toggle="dropdown" className="dropdown-toggle" href="#">
                  <i className="fa fa-list-ol"></i>
                  <span className="caret"></span>
                </a>
                <ul className="dropdown-menu">
                  {pageSizeSelect.map((limit, index) => (
                    <li key={index}>
                      <a className="fa33" onClick={() => changeLimit(limit)}>{limit}</a>
                    </li>
                  ))}
                </ul>
              </li>
              <li className="dropdown pull-right">
                <a data-toggle="dropdown" className="dropdown-toggle" href="#">
                  <i className="fa fa-sort-alpha-asc"></i>
                  <span className="caret"></span>
                </a>
                <ul id="drop-down" className="dropdown-menu">
                  <li>
                    <a className="fa33" onClick={() => handleSort('folderName')}>
                      {'name' | translate}
                      {sort.folderName === 1 ? <i className="fa fa-arrow-down"></i> : null}
                      {sort.folderName === -1 ? <i className="fa fa-arrow-up"></i> : null}
                    </a>
                  </li>
                  <li>
                    <a className="fa33" onClick={() => handleSort('date')}>
                      {'created' | translate}
                      {sort.date === 1 ? <i className="fa fa-arrow-down"></i> : null}
                      {sort.date === -1 ? <i className="fa fa-arrow-up"></i> : null}
                    </a>
                  </li>
                  <li>
                    <a className="fa33" onClick={() => handleSort('description')}>
                      {'description' | translate}
                      {sort.description === 1 ? <i className="fa fa-arrow-down"></i> : null}
                      {sort.description === -1 ? <i className="fa fa-arrow-up"></i> : null}
                    </a>
                  </li>
                </ul>
              </li>
            </ul>
            <div className="table-responsive">
              <SortableTable headers={headers} data={folders} />
            </div>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12 text-center">
          <Paging {...pagingSettings} onPageChange={getNextPage} showPrevNext showFirstLast hideIfEmpty ulClass="pagination" />
        </div>
      </div>
    </div>
  );
};

const headers = [
  { key: 'index', label: '#' },
  { key: 'date', label: 'Create Date' },
  { key: 'name', label: 'Name' },
  { key: 'view', label: 'View' },
  { key: 'description', label: 'Description' },
  { key: 'files', label: 'Files' },
  { key: 'status', label: 'Status' },
  { key: 'actions', label: 'Actions' }
];

export default ClientZoneMyFolders;