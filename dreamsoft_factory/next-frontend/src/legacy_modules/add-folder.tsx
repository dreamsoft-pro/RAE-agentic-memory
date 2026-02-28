/**
 * Service: add-folder
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

interface AddFolderProps {
  functionType: string;
  modalForm: {
    folderName: string;
    description: string;
  };
  save: () => void;
}

const AddFolder: React.FC<AddFolderProps> = ({ functionType, modalForm, save }) => {
  const { t } = useTranslation();

  return (
    <div className="modal-header">
      <h4 className="modal-title">
        {functionType === 'add' ? t('add_folder') : t('edit_folder')}
      </h4>
    </div>
    <div className="modal-body">
      <div className="row">
        <div className="col-xs-10 col-xs-offset-1">
          <form className="form-horizontal" role="form" onSubmit={save}>
            <div className="form-body">
              <div className="form-group">
                <label htmlFor="my-folder-name" className="col-md-3 control-label">
                  {t('name')}
                </label>
                <div className="col-md-9">
                  <input
                    type="text"
                    className="form-control"
                    value={modalForm.folderName}
                    onChange={(e) => modalForm.folderName = e.target.value}
                    placeholder={t('name')}
                    required
                    id="my-folder-name"
                  />
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="my-folder-description" className="col-md-3 control-label">
                  {t('description')}
                </label>
                <div className="col-md-9">
                  <textarea
                    className="form-control"
                    value={modalForm.description}
                    onChange={(e) => modalForm.description = e.target.value}
                    placeholder={t('description')}
                    id="my-folder-description"
                  />
                </div>
              </div>
              <div className="form-group">
                <div className="col-md-3 col-md-offset-9">
                  <button type="submit" className="btn btn-success btn-block btn-submit">
                    {t('save')}
                  </button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div className="modal-footer">
      <button className="btn btn-default" onClick={() => {}}>
        {t('close')}
      </button>
    </div>
  );
};

export default AddFolder;