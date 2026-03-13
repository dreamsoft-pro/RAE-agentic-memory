/**
 * Service: select-product
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

const SelectProduct = ({ allTypes, currentLang }) => {
  const { t } = useTranslation();
  const [selectedTypeID, setSelectedTypeID] = useState('');

  const handleSelectChange = (event) => {
    setSelectedTypeID(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission logic here
  };

  return (
    <div className="panel panel-default" id="panel-select-other-product">
      <div className="panel-heading">
        <h3 className="panel-title">{t('select_product_type')}</h3>
      </div>
      <div className="panel-body">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <div className="col-md-9">
              <select className="form-control" value={selectedTypeID} onChange={handleSelectChange}>
                <option value="">{t('select')}</option>
                {allTypes.map((item) => (
                  <option key={item.ID} value={item.ID}>
                    {item.names[currentLang.code]}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="form-group">
            <div className="col-md-3">
              <button type="submit" className="btn btn-success btn-block btn-submit">
                <i className="fa fa-arrow-right" aria-hidden="true"></i>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SelectProduct;