/**
 * Service: client-zone-invoice-data
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface FormData {
    companyName: string;
    city: string;
    street: string;
    house: string;
    apartment?: string;
    countryCode?: string;
    zipcode: string;
}

interface Props {
    form: FormData;
    countries: Array<{ code: string, name_pl: string }>;
    onSubmit: () => void;
    translate: (key: string) => string;
}

const ClientZoneInvoiceForm: React.FC<Props> = ({ form, countries, onSubmit, translate }) => {
    return (
        <div className="panel panel-default">
            <div className="panel-heading">
                <h2 className="panel-title">
                    {translate('data_to_invoice')} - {form.companyName} - {form.city}, {form.street} {form.house}
                    {form.apartment && <span>/{{form.apartment}}</span>}
                </h2>
            </div>
            <div className="panel-body">
                <form onSubmit={onSubmit} className="form-horizontal" role="form">
                    <div className="form-group">
                        <label htmlFor="invoice-company-name" className="col-md-3 control-label">
                            {translate('company_name')} *
                        </label>
                        <div className="col-md-9">
                            <input 
                                type="text" 
                                id="invoice-company-name" 
                                className="form-control" 
                                required 
                                value={form.companyName} 
                                onChange={(e) => console.log(e.target.value)} 
                                placeholder={translate('company_name')}
                            />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="invoice-city" className="col-md-3 control-label">
                            {translate('city')} *
                        </label>
                        <div className="col-md-9">
                            <input 
                                type="text" 
                                id="invoice-city" 
                                className="form-control" 
                                required 
                                value={form.city} 
                                onChange={(e) => console.log(e.target.value)} 
                                placeholder={translate('city')}
                            />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="invoice-nip" className="col-md-3 control-label">
                            {translate('nip')} *
                        </label>
                        <div className="col-md-9">
                            <input 
                                type="text" 
                                id="invoice-nip" 
                                className="form-control" 
                                required 
                                value={form.nip} 
                                onChange={(e) => console.log(e.target.value)} 
                                placeholder={translate('nip')}
                            />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="invoice-street" className="col-md-3 control-label">
                            {translate('street')} *
                        </label>
                        <div className="col-md-9">
                            <input 
                                type="text" 
                                id="invoice-street" 
                                className="form-control" 
                                required 
                                value={form.street} 
                                onChange={(e) => console.log(e.target.value)} 
                                placeholder={translate('street')}
                            />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="invoice-no-house" className="col-md-3 control-label">
                            {translate('no_house')} *
                        </label>
                        <div className="col-md-9">
                            <input 
                                type="text" 
                                id="invoice-no-house" 
                                className="form-control" 
                                required 
                                value={form.house} 
                                onChange={(e) => console.log(e.target.value)} 
                                placeholder={translate('no_house')}
                            />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="invoice-flat-number" className="col-md-3 control-label">
                            {translate('flat_number')}
                        </label>
                        <div className="col-md-9">
                            <input 
                                type="text" 
                                id="invoice-flat-number" 
                                className="form-control" 
                                value={form.apartment} 
                                onChange={(e) => console.log(e.target.value)} 
                                placeholder={translate('flat_number')}
                            />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="invoice-country" className="col-md-3 control-label">
                            {translate('country')}
                        </label>
                        <div className="col-md-9">
                            <select 
                                id="invoice-country" 
                                className="form-control" 
                                required 
                                value={form.countryCode} 
                                onChange={(e) => console.log(e.target.value)}>
                                {countries.map(country => (
                                    <option key={country.code} value={country.code}>{country.name_pl}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                    <div className="form-group">
                        <div className="col-md-3 col-md-offset-9">
                            <button type="submit" className="btn btn-success btn-block btn-submit">
                                {translate('save')}
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ClientZoneInvoiceForm;