/**
 * Service: join-deliveries
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

interface Delivery {
  ID: number;
  names: { [key: string]: string };
}

interface CollectionPoint {
  ID: number;
  langs: { [key: string]: { name: string } };
}

interface Props {
  activeAddressToJoin: any[];
  deliveries: Delivery[];
  collectionPoints: CollectionPoint[];
  summary: {
    selectedDelivery: { names: { [key: string]: string } };
    overallWeight: number;
    numberOfPackages: number;
    priceGross: number;
  };
  currentLang: { code: string };
  currentCurrency: { code: string };
}

const JoinDeliveriesModal: React.FC<Props> = ({ activeAddressToJoin, deliveries, collectionPoints, summary, currentLang, currentCurrency }) => {
  const [joinDeliveryID, setJoinDeliveryID] = useState(activeAddressToJoin[0].deliveryID);
  const [collectionPointID, setCollectionPointID] = useState<number | null>(null);
  const { t } = useTranslation();

  const changeDelivery = () => {
    // Handle delivery change logic here
  };

  const changeCollectionPoint = () => {
    // Handle collection point change logic here
  };

  const save = () => {
    // Handle form submission logic here
  };

  return (
    <>
      <div className="modal-header">
        <h4>{t('merge_deliveries')}</h4>
      </div>
      <div className="modal-body">
        <div className="row">
          <div className="col-md-6">
            <form onSubmit={save}>
              <div className="input-group">
                <select
                  className="form-control"
                  value={joinDeliveryID}
                  onChange={(e) => setJoinDeliveryID(parseInt(e.target.value))}
                  onBlur={changeDelivery}
                >
                  {deliveries.map((item) => (
                    <option key={item.ID} value={item.ID}>
                      {item.names[currentLang.code]}
                    </option>
                  ))}
                </select>
              </div>
              <div className="input-group">
                {collectionPoints.length > 0 && (
                  <select
                    className="form-control"
                    value={collectionPointID || ''}
                    onChange={(e) => setCollectionPointID(parseInt(e.target.value))}
                    onBlur={changeCollectionPoint}
                  >
                    {collectionPoints.map((item) => (
                      <option key={item.ID} value={item.ID}>
                        {item.langs[currentLang.code].name}
                      </option>
                    ))}
                  </select>
                )}
              </div>
              <div className="input-group">
                <button type="submit" className="btn btn-success">
                  {t('save')}
                </button>
              </div>
            </form>
          </div>
          <div className="col-md-6">
            <p>{summary.selectedDelivery.names[currentLang.code]}</p>
            <p>{t('total_weight')}: {summary.overallWeight} kg</p>
            <p>{t('packages')}: {summary.numberOfPackages}</p>
            <p>{t('price')}: <b>{summary.priceGross} {currentCurrency.code}</b></p>
          </div>
        </div>
      </div>
      <div className="modal-footer">
        <button className="btn btn-default" onClick={() => {}}>
          {t('close')}
        </button>
      </div>
    </>
  );
};

export default JoinDeliveriesModal;