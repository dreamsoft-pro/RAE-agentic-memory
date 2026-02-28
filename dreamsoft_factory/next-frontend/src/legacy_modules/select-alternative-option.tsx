/**
 * Service: select-alternative-option
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

interface Option {
  name: string;
}

interface Props {
  selectedOptionInstance: Option[];
  altOptions: Option[];
  chooseAltOption: (option: Option) => void;
  closeModal: () => void;
}

const SelectAlternativeOption: React.FC<Props> = ({ selectedOptionInstance, altOptions, chooseAltOption, closeModal }) => {
  const { t } = useTranslation();

  return (
    <div className="modal-header">
      <h4 className="modal-title">
        {t('alternative_options')}: {selectedOptionInstance[0]?.name}
      </h4>
    </div>
    <div className="modal-body">
      <div className="row">
        <div className="col-md-12">
          <div className="form-body">
            {altOptions.map((option, index) => (
              <div key={index} className="alternateOption" onClick={() => chooseAltOption(option)}>
                {option.name}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
    <div className="modal-footer">
      <button className="btn btn-default" onClick={closeModal}>{t('close')}</button>
    </div>
  );
};

export default SelectAlternativeOption;