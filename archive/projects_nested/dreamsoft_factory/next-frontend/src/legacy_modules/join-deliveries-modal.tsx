/**
 * Service: join-deliveries-modal
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

interface Delivery {
  ID: number;
  names: { [key: string]: string };
}

interface CollectionPoint {
  ID: number;
  langs: { [key: string]: { name: string } };
}

interface Summary {
  selectedDelivery: { names: { [key: string]: string } };
  overallWeight: number;
  numberOfPackages: number;
}

const JoinDeliveriesModal: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [joinDeliveryID, setJoinDeliveryID] = useState<number | null>(null);
  const [collectionPointID, setCollectionPointID] = useState<number | null>(null);
  const [deliveries, setDeliveries] = useState<Delivery[]>([]);
  const [collectionPoints, setCollectionPoints] = useState<CollectionPoint[]>([]);
  const [summary, setSummary] = useState<Summary>({
    selectedDelivery: { names: {} },
    overallWeight: 0,
    numberOfPackages: 0,
  });

  useEffect(() => {
    axios.get('/api/deliveries').then(response => {
      setDeliveries(response.data);
    });

    axios.get('/api/collectionPoints').then(response => {
      setCollectionPoints(response.data);
    });
  }, []);

  const changeDelivery = () => {
    // Fetch summary data based on joinDeliveryID
    if (joinDeliveryID) {
      axios.get(`/api/deliverySummary/${joinDeliveryID}`).then(response => {
        setSummary(response.data);
      });
    }
  };

  const changeCollectionPoint = () => {
    // Handle collection point change if needed
  };

  const save = async (event: React.FormEvent) => {
    event.preventDefault();
    // Perform save operation with joinDeliveryID and collectionPointID
  };

  return (
    <div>
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
                  value={joinDeliveryID || ''}
                  onChange={(e) => setJoinDeliveryID(parseInt(e.target.value))}
                  onBlur={changeDelivery}
                >
                  {deliveries.map(delivery => (
                    <option key={delivery.ID} value={delivery.ID}>
                      {delivery.names[i18n.language]}
                    </option>
                  ))}
                </select>
              </div>
              <div className="input-group">
                <select
                  className="form-control"
                  value={collectionPointID || ''}
                  onChange={(e) => setCollectionPointID(parseInt(e.target.value))}
                  onBlur={changeCollectionPoint}
                >
                  {collectionPoints.map(point => (
                    <option key={point.ID} value={point.ID}>
                      {point.langs[i18n.language].name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="input-group">
                <button type="submit" className="btn btn-success">{t('save')}</button>
              </div>
            </form>
          </div>
          <div className="col-md-6">
            {summary.selectedDelivery.names[i18n.language]}<br />
            {t('total_weight')}: {summary.overallWeight} kg<br />
            {t('packages')}: {summary.numberOfPackages}<br /><br />
          </div>
        </div>
      </div>
    </div>
  );
};

export default JoinDeliveriesModal;