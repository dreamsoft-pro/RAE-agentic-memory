/**
 * Service: client-zone-data
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface FormData {
    login: string;
    name: string;
    lastname: string;
    city: string;
    street: string;
    house: string;
    apartment: string;
    countryCode: string;
    zipcode: string;
    telephone: string;
    smsAgree: boolean;
    advAgree: boolean;
}

interface Props {
    form: FormData;
    countries: any[]; // Adjust the type according to your data structure
    currentLang: any; // Adjust the type according to your data structure
    edit: () => void;
    updateAreaCode: () => void;
}

const ClientZoneData: React.FC<Props> = ({ form, countries, currentLang, edit, updateAreaCode }) => {
    return (
        <div className="panel panel-default">
            <div className="panel-heading">
                <h2 className="panel-title">
                    {`your_data` | translate} - {form.city}, {form.street} {form.house}<span>{form.apartment && `/${form.apartment}`}</span>
                </h2>
            </div>
            <div className="panel-body">
                <form className="form-horizontal" role="form" onSubmit={edit}>
                    <div className="form-group">
                        <label className="col-md-3 control-label">{`login` | translate}</label>
                        <div className="col-md-9">
                            <input className="form-control" disabled={true} value={form.login} />
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="col-md-3 control-label" htmlFor="user-firstname">{`firstname` | translate}</label>
                        <div className="col-md-9">
                            <input className="form-control" value={form.name} onChange={(e) => handleChange(e, 'name')} placeholder={`firstname` | translate} required id="user-firstname" />
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="col-md-3 control-label" htmlFor="user-lastname">{`lastname` | translate}</label>
                        <div className="col-md-9">
                            <input className="form-control" value={form.lastname} onChange={(e) => handleChange(e, 'lastname')} placeholder={`lastname` | translate} required id="user-lastname" />
                        </div>
                    </div>

                    {/* Continue with other form fields... */}

                </form>
            </div>
        </div>
    );
};

export default ClientZoneData;