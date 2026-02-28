/**
 * Service: client-zone-delivery-data
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

const ClientZoneDeliveryData: React.FC = () => {
    const { t, i18n } = useTranslation();

    return (
        <div>
            <form className="form-horizontal" role="form" onSubmit={add}>
                <fieldset>
                    <legend>{t('add_delivery_address')}</legend>
                    <div className="form-group">
                        <label htmlFor="delivery-address-firstname" className="col-md-3 control-label">{t('firstname')}</label>
                        <div className="col-md-9">
                            <input type="text" className="form-control" id="delivery-address-firstname" placeholder={t('firstname')} required />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="delivery-address-lastname" className="col-md-3 control-label">{t('lastname')}</label>
                        <div className="col-md-9">
                            <input type="text" className="form-control" id="delivery-address-lastname" placeholder={t('lastname')} required />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="delivery-address-company-name" className="col-md-3 control-label">{t('company_name')}</label>
                        <div className="col-md-9">
                            <input type="text" className="form-control" id="delivery-address-company-name" placeholder={t('company_name')} />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="delivery-address-street" className="col-md-3 control-label">{t('street')}</label>
                        <div className="col-md-9">
                            <input type="text" className="form-control" id="delivery-address-street" placeholder={t('street')} required />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="delivery-address-no-house" className="col-md-3 control-label">{t('no_house')}</label>
                        <div className="col-md-9">
                            <input type="text" className="form-control" id="delivery-address-no-house" placeholder={t('no_house')} required />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="delivery-address-flat-number" className="col-md-3 control-label">{t('flat_number')}</label>
                        <div className="col-md-9">
                            <input type="text" className="form-control" id="delivery-address-flat-number" placeholder={t('flat_number')} />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="delivery-address-zipcode" className="col-md-3 control-label">{t('postal_code')}</label>
                        <div className="col-md-9">
                            <input type="text" className="form-control" id="delivery-address-zipcode" placeholder={t('postal_code')} required />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="delivery-address-city" className="col-md-3 control-label">{t('city')}</label>
                        <div className="col-md-9">
                            <input type="text" className="form-control" id="delivery-address-city" placeholder={t('city')} required />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="delivery-address-country" className="col-md-3 control-label">{t('country')}</label>
                        <div className="col-md-9">
                            <select id="delivery-address-country" className="form-control">
                                {countries.map(country => (
                                    <option key={country.code} value={country.code}>{t(`name_${i18n.language}` as any)}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="delivery-address-phone" className="col-md-3 control-label">{t('phone')}</label>
                        <div className="col-md-6">
                            <input type="tel" className="form-control" id="delivery-address-phone" />
                        </div>
                    </div>
                </fieldset>
                <div className="form-group">
                    <div className="col-md-3 col-md-offset-9">
                        <button type="submit" className="btn btn-success btn-block">{t('save')}</button>
                    </div>
                </div>
            </form>

            <div className="panel panel-default">
                <div className="panel-heading">
                    <h2 className="panel-title">{t('Delivery_addresses')}</h2>
                </div>
                <div className="panel-body">
                    <table className="table table-hover table-responsive">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>{t('name')}</th>
                                <th>{t('default')}</th>
                                <th>{t('actions')}</th>
                            </tr>
                        </thead>
                        <tbody>
                            {addresses.map(address => (
                                <tr key={address.ID}>
                                    <td className="col-address-id">{address.ID}</td>
                                    <td className="col-address-name">{`${address.city}, ${address.street} ${address.house}<span>${address.apartment ? `/${address.apartment}` : ''}</span>`}</td>
                                    <td className="col-address-default">
                                        {address.default === 1 ? t('yes') : t('no')}
                                    </td>
                                    <td className="col-address-actions">
                                        <button className="btn btn-primary" onClick={() => addressEdit(address)}>{t('edit')}</button>
                                        {address.default !== 1 && (
                                            <button className="btn btn-default" onClick={() => addressRemove(address)}>{t('remove')}</button>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default ClientZoneDeliveryData;