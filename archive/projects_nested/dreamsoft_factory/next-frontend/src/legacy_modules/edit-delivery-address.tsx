/**
 * Service: edit-delivery-address
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface ModalFormProps {
    modalForm: {
        name: string;
        lastname: string;
        companyName: string;
        zipcode: string;
        city: string;
        countryCode: string;
        areaCode: string;
        telephone: string;
        default: number;
        street: string;
        house: string;
        apartment: string;
    };
    countries: { code: string, name_pl: string }[];
    updateAreaCode: (form: any) => void;
    isCountryCode: (form: any) => boolean;
}

const EditDeliveryAddress: React.FC<ModalFormProps> = ({ modalForm, countries, updateAreaCode, isCountryCode }) => {
    return (
        <div className="modal-header">
            <h4 className="modal-title">{`${'addresses' | translate} - ${modalForm.city}, ${modalForm.street} ${modalForm.house}<span>{modalForm.apartment && `/${modalForm.apartment`}</span>`}</h4>
        </div>
        <div className="modal-body">
            <div className="row">
                <div className="col-xs-10 col-xs-offset-1">
                    <form role="form" onSubmit={() => save()}>
                        <div className="form-body">
                            <div className="form-group">
                                <label htmlFor="mf-address-firstname" className="col-md-3 control-label">{'firstname' | translate}</label>
                                <div className="col-md-9">
                                    <input type="text" className="form-control" value={modalForm.name} onChange={(e) => setModalForm({ ...modalForm, name: e.target.value })} placeholder={'firstname' | translate} required id="mf-address-firstname" />
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="mf-address-lastname" className="col-md-3 control-label">{'lastname' | translate}</label>
                                <div className="col-md-9">
                                    <input type="text" className="form-control" value={modalForm.lastname} onChange={(e) => setModalForm({ ...modalForm, lastname: e.target.value })} placeholder={'lastname' | translate} required id="mf-address-lastname" />
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="mf-address-company-name" className="col-md-3 control-label">{'company_name' | translate}</label>
                                <div className="col-md-9">
                                    <input type="text" className="form-control" value={modalForm.companyName} onChange={(e) => setModalForm({ ...modalForm, companyName: e.target.value })} id="mf-address-company-name" />
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="mf-address-zipcode" className="col-md-3 control-label">{'postal_code' | translate}</label>
                                <div className="col-md-9">
                                    <input type="text" className="form-control" value={modalForm.zipcode} onChange={(e) => setModalForm({ ...modalForm, zipcode: e.target.value })} placeholder={'postal_code' | translate} id="mf-address-zipcode" />
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="mf-address-city" className="col-md-3 control-label">{'city' | translate}</label>
                                <div className="col-md-9">
                                    <input type="text" className="form-control" value={modalForm.city} onChange={(e) => setModalForm({ ...modalForm, city: e.target.value })} placeholder={'city' | translate} id="mf-address-city" />
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="mf-address-country" className="col-md-3 control-label">{'country' | translate}</label>
                                <div className="col-md-9">
                                    <select id="mf-address-country" className="form-control" value={modalForm.countryCode} onChange={(e) => setModalForm({ ...modalForm, countryCode: e.target.value })}>
                                        {countries.map(country => (
                                            <option key={country.code} value={country.code}>{country.name_pl}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="mf-address-phone" className="col-md-3 control-label">{'phone' | translate}</label>
                                <div className="col-md-2">
                                    <div className="input-group">
                                        <span className="input-group-addon"><i className="fa fa-plus"></i></span>
                                        <input type="tel" disabled={isCountryCode(modalForm)} value={modalForm.areaCode} onChange={(e) => setModalForm({ ...modalForm, areaCode: e.target.value })} className="form-control" />
                                    </div>
                                </div>
                                <div className="col-md-7">
                                    <input type="tel" className="form-control" value={modalForm.telephone} onChange={(e) => setModalForm({ ...modalForm, telephone: e.target.value })} placeholder={'phone' | translate} id="mf-address-phone" />
                                </div>
                            </div>
                            <div className="form-group">
                                <div className="col-sm-offset-3 col-sm-7">
                                    <div className="checkbox">
                                        <label>
                                            <input type="checkbox" disabled={modalForm.default === 1} checked={modalForm.default === 1} onChange={(e) => setModalForm({ ...modalForm, default: e.target.checked ? 1 : 0 })} />
                                            {'default_shipping_address' | translate}
                                        </label>
                                    </div>
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="mf-address-street" className="col-md-3 control-label">{'street' | translate}</label>
                                <div className="col-md-9">
                                    <input type="text" className="form-control" value={modalForm.street} onChange={(e) => setModalForm({ ...modalForm, street: e.target.value })} placeholder={'street' | translate} id="mf-address-street" />
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="mf-address-no-house" className="col-md-3 control-label">{'no_house' | translate}</label>
                                <div className="col-md-9">
                                    <input type="text" className="form-control" value={modalForm.house} onChange={(e) => setModalForm({ ...modalForm, house: e.target.value })} placeholder={'no_house' | translate} id="mf-address-no-house" />
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="mf-address-apartment" className="col-md-3 control-label">{'flat_number' | translate}</label>
                                <div className="col-md-9">
                                    <input type="text" className="form-control" value={modalForm.apartment} onChange={(e) => setModalForm({ ...modalForm, apartment: e.target.value })} placeholder={'flat_number' | translate} id="mf-address-apartment" />
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <div className="modal-footer">
            <button className="btn btn-default" onClick={() => onDismiss()}>{'close' | translate}</button>
        </div>
    );
};

export default EditDeliveryAddress;