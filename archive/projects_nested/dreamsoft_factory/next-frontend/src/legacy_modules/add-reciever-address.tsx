/**
 * Service: add-reciever-address
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const AddReceiverAddress: React.FC = () => {
    const [form, setForm] = React.useState({
        lastname: '',
        house: '',
        zipcode: '',
        name: '',
        street: '',
        apartment: '',
        city: '',
        areaCode: '',
        telephone: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.id]: e.target.value });
    };

    return (
        <div>
            <div className="modal-header">
                <h4 className="modal-title">{'add_new_address' | translate}</h4>
            </div>
            <div className="modal-body">
                <div className="row">
                    <div className="col-md-12">
                        <div className="alert alert-info">{'no_address_in_cart' | translate}</div>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-12">
                        <fieldset>
                            <div className="row">
                                <div className="col-md-6">
                                    <div className="form-group firstName">
                                        <label htmlFor="mf-address-firstname" className="col-md-5 control-label">* {'firstname' | translate}</label>
                                        <div className="col-md-7">
                                            <input type="text" id="mf-address-firstname" className="form-control" value={form.name} onChange={handleChange} placeholder={'firstname' | translate} required data-toggle="validator" />
                                        </div>
                                    </div>
                                    <div className="form-group street">
                                        <label htmlFor="mf-address-street" className="col-md-5 control-label">* {'street' | translate}</label>
                                        <div className="col-md-7">
                                            <input type="text" id="mf-address-street" className="form-control" value={form.street} onChange={handleChange} placeholder={'street' | translate} required data-toggle="validator" />
                                        </div>
                                    </div>
                                    <div className="form-group flat-no">
                                        <label htmlFor="mf-address-flat-number" className="col-md-5 control-label">{'flat_number' | translate}</label>
                                        <div className="col-md-7">
                                            <input type="text" id="mf-address-flat-number" className="form-control" value={form.apartment} onChange={handleChange} placeholder={'flat_number' | translate} />
                                        </div>
                                    </div>
                                    <div className="form-group city">
                                        <label htmlFor="mf-address-city" className="col-md-5 control-label">* {'city' | translate}</label>
                                        <div className="col-md-7">
                                            <input type="text" id="mf-address-city" className="form-control" value={form.city} onChange={handleChange} placeholder={'city' | translate} required data-toggle="validator" />
                                        </div>
                                    </div>
                                </div>
                                <div className="col-md-6">
                                    <div className="form-group lastname">
                                        <label htmlFor="mf-address-lastname" className="col-md-5 control-label">* {'lastname' | translate}</label>
                                        <div className="col-md-7">
                                            <input type="text" id="mf-address-lastname" className="form-control" value={form.lastname} onChange={handleChange} placeholder={'lastname' | translate} required data-toggle="validator" />
                                        </div>
                                    </div>
                                    <div className="form-group house-no">
                                        <label htmlFor="mf-address-house" className="col-md-5 control-label">* {'no_house' | translate}</label>
                                        <div className="col-md-7">
                                            <input type="text" id="mf-address-house" className="form-control" value={form.house} onChange={handleChange} placeholder={'no_house' | translate} required data-toggle="validator" />
                                        </div>
                                    </div>
                                    <div className="form-group postal-code">
                                        <label htmlFor="mf-address-zipcode" className="col-md-5 control-label">* {'postal_code' | translate}</label>
                                        <div className="col-md-7">
                                            <input type="text" id="mf-address-zipcode" className="form-control" value={form.zipcode} onChange={handleChange} placeholder={'postal_code' | translate} required data-toggle="validator" />
                                        </div>
                                    </div>
                                    <div className="form-group phone">
                                        <label htmlFor="mf-address-area-code" className="col-md-5 control-label">{'phone' | translate}</label>
                                        <div className="col-md-2">
                                            <input type="text" id="mf-address-area-code" className="form-control" value={form.areaCode} onChange={(e) => setForm({ ...form, areaCode: e.target.value })} placeholder="+" />
                                        </div>
                                        <div className="col-md-5">
                                            <input type="text" id="mf-address-telephone" className="form-control" value={form.telephone} onChange={handleChange} required />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </fieldset>
                    </div>
                </div>
            </div>
            <div className="modal-footer">
                <button type="submit" className="btn btn-success btn-submit">{'add' | translate}</button>
                <button onClick={() => { /* close logic */ }} className="btn btn-default">{'close' | translate}</button>
            </div>
        </div>
    );
};

export default AddReceiverAddress;