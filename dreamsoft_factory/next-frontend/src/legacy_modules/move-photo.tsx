/**
 * Service: move-photo
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

interface Props {
  functionType?: string;
  folders?: any[];
  form?: any;
  save?: () => void;
}

const MovePhoto: React.FC<Props> = ({ functionType, folders, form, save }) => {
  const { t } = useTranslation();

  return (
    <div className="modal-header">
      <h4 className="modal-title">
        {functionType === 'move' ? t('move') : functionType === 'copy' ? t('copy') : ''}
      </h4>
    </div>
  );
};

export default MovePhoto;