/**
 * Service: add-invoice-address
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface FormData {
    name: string;
    lastname: string;
    companyName?: string;
    street: string;
    house: string;
    apartment?: string;
    zipcode: string;
    city: string;
    countryCode: string;
}

interface Props {
    form: FormData;
    countries: { code: string, name_pl: string }[];
    saveAddress: () => void;
    onDismiss: () => void;
}

const AddInvoiceAddress: React.FC<Props> = ({ form, countries, saveAddress, onDismiss }) => (
    <form className="form-horizontal" onSubmit={saveAddress}>
        <div className="modal-header">
            <h4 className="modal-title">{'add_new_address' | translate}</h4>
        </div>
        <div className="modal-body">
            <div className="row">
                <div className="col-md-12">
                    <div className="alert alert-info">{'no_invoice_address_in_cart' | translate}</div>
                </div>
            </div>
            <div className="row">
                <div className="col-md-12">
                    <fieldset>
                        <div className="form-group name">
                            <label className="col-md-3 control-label" htmlFor="invoice-name">
                                {'firstname' | translate} {form.companyName ? '' : '*'}
                            </label>
                            <div className="col-md-7">
                                <input type="text" 
                                       value={form.name} 
                                       onChange={(e) => setForm({ ...form, name: e.target.value })} 
                                       className="form-control" 
                                       placeholder={'firstname' | translate} 
                                       required={!form.companyName} />
                            </div>
                        </div>
                        <div className="form-group lastname">
                            <label className="col-md-3 control-label" htmlFor="invoice-lastname">
                                {'lastname' | translate} {form.companyName ? '' : '*'}
                            </label>
                            <div className="col-md-7">
                                <input type="text" 
                                       value={form.lastname} 
                                       onChange={(e) => setForm({ ...form, lastname: e.target.value })} 
                                       className="form-control" 
                                       placeholder={'lastname' | translate} 
                                       required={!form.companyName} />
                            </div>
                        </div>
                        <div className="form-group companyName">
                            <label className="col-md-3 control-label" htmlFor="invoice-companyName">
                                {'company_name' | translate} {(!form.name || !form.lastname) ? '*' : ''}
                            </label>
                            <div className="col-md-7">
                                <input type="text" 
                                       value={form.companyName} 
                                       onChange={(e) => setForm({ ...form, companyName: e.target.value })} 
                                       className="form-control" 
                                       placeholder={'company_name' | translate} 
                                       required={!form.name || !form.lastname} />
                            </div>
                        </div>
                        <div className="form-group add-street">
                            <label className="col-md-3 control-label" htmlFor="invoice-street">
                                {'street' | translate} *
                            </label>
                            <div className="col-md-7">
                                <input type="text" 
                                       value={form.street} 
                                       onChange={(e) => setForm({ ...form, street: e.target.value })} 
                                       className="form-control" 
                                       placeholder={'street' | translate} 
                                       required />
                            </div>
                        </div>
                        <div className="form-group add-house-no">
                            <label className="col-md-3 control-label" htmlFor="invoice-no-house">
                                {'no_house' | translate} *
                            </label>
                            <div className="col-md-7">
                                <input type="text" 
                                       value={form.house} 
                                       onChange={(e) => setForm({ ...form, house: e.target.value })} 
                                       className="form-control" 
                                       placeholder={'no_house' | translate} 
                                       required />
                            </div>
                        </div>
                        <div className="form-group add-post-code">
                            <label className="col-md-3 control-label" htmlFor="invoice-apartment-number">
                                {'apartment_number' | translate}
                            </label>
                            <div className="col-md-7">
                                <input type="text" 
                                       value={form.apartment} 
                                       onChange={(e) => setForm({ ...form, apartment: e.target.value })} 
                                       className="form-control" 
                                       placeholder={'apartment_number' | translate} />
                            </div>
                        </div>
                        <div className="form-group add-post-code">
                            <label className="col-md-3 control-label" htmlFor="invoice-zipcode">
                                {'postal_code' | translate} *
                            </label>
                            <div className="col-md-7">
                                <input type="text" 
                                       value={form.zipcode} 
                                       onChange={(e) => setForm({ ...form, zipcode: e.target.value })} 
                                       className="form-control" 
                                       placeholder={'postal_code' | translate} 
                                       required />
                            </div>
                        </div>
                        <div className="form-group ad-city">
                            <label className="col-md-3 control-label" htmlFor="invoice-city">
                                {'city' | translate} *
                            </label>
                            <div className="col-md-7">
                                <input type="text" 
                                       value={form.city} 
                                       onChange={(e) => setForm({ ...form, city: e.target.value })} 
                                       className="form-control" 
                                       placeholder={'city' | translate} 
                                       required />
                            </div>
                        </div>
                        <div className="form-group ad-country">
                            <label className="col-md-3 control-label" htmlFor="invoice-countryCode">
                                {'country' | translate} *
                            </label>
                            <div className="col-md-7">
                                <select onChange={(e) => setForm({ ...form, countryCode: e.target.value })} required>
                                    {countries.map(country => (
                                        <option key={country.code} value={country.code}>{country.name_pl}</option>
                                    ))}
                                </select>
                            </div>
                        </div>
                    </fieldset>
                </div>
            </div>
        </div>
        <div className="modal-footer">
            <button type="submit" className="btn btn-success btn-submit">
                {'add' | translate}
            </button>
            <button className="btn btn-default" onClick={onDismiss}>{'close' | translate}</button>
        </div>
    </form>
);

export default AddInvoiceAddress;