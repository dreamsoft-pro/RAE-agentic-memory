/**
 * Service: without_registration
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

const NoRegistrationForm: React.FC = () => {
    const { t, i18n } = useTranslation();

    // Assuming noRegisterForm and countries are defined elsewhere in the state management or props
    const [noRegisterForm, setNoRegisterForm] = React.useState({
        name: '',
        lastname: '',
        ad_apartment: '',
        ad_zipcode: '',
        ad_city: '',
        ad_countryCode: '',
        ad_telephone: '',
        hasFvAddress: false,
        fv_companyName: '',
        fv_nip: '',
        fv_street: '',
        // Add other fields as necessary
    });

    const [countries] = React.useState([]); // This should be populated with actual data based on your application logic

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setNoRegisterForm({ ...noRegisterForm, [name]: value });
    };

    const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setNoRegisterForm({ ...noRegisterForm, hasFvAddress: e.target.checked });
    };

    const selectCountry = (field: string, value: any) => {
        // Implement the logic to handle country selection
    };

    return (
        <form className="form-horizontal" role="form" onSubmit={() => addNonRegister()}>
            <div className="form-group firstname">
                <label htmlFor="no-register-firstname" className="col-sm-3 control-label">
                    {t('firstname')} {/* Assuming 'firstname' is a translatable key */}
                </label>
                <div className="col-sm-7">
                    <input type="text" name="name" value={noRegisterForm.name} onChange={handleChange} className="form-control" placeholder={t('firstname')} id="no-register-firstname" />
                </div>
            </div>
            {/* Repeat similar structures for other form fields */}
            <div className="col-md-12 text-right">
                <button type="submit" className="btn btn-success btn-lg btn-submit">
                    {t('go_to_payment_confirm')} {/* Assuming 'go_to_payment_confirm' is a translatable key */}
                </button>
            </div>
            <p>* {t('required_field')}</p> {/* Assuming 'required_field' is a translatable key */}
        </form>
    );
};

export default NoRegistrationForm;