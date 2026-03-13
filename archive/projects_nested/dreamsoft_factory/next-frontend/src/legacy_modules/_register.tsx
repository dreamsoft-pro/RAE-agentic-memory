/**
 * Service: _register
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

const RegisterComponent: React.FC = () => {
    const { t, i18n } = useTranslation();

    return (
        <div className="container" id="content-register">
            <div className="row">
                <div className="col-xs-12">
                    <h1 className="page-header">{t('create_account')}</h1>
                </div>
            </div>
            <div className="row">
                <div className="col-md-7">
                    <div className="panel panel-default panel-register">
                        <div className="panel-heading">
                            <h3 className="panel-title">{t('register')}</h3>
                        </div>
                        <div className="panel-body">
                            <div className="well well-sm">{t('register_text_1')}</div>
                            {/* build:include ../../../views/_forms/register.html */}
                            This will be replaced by the content of description.html
                            {/* /build */}
                        </div>
                    </div>
                </div>
                <div className="col-md-5">
                    <div className="panel panel-default panel-login">
                        <div className="panel-heading">
                            <h3 className="panel-title">{t('already_have_account')}: ?</h3>
                        </div>
                        <div className="panel-body">
                            <div className="well well-sm">{t('register_if_not_have_account')}</div>
                            {/* build:include ../../../views/_forms/login.html */}
                            This will be replaced by the content of description.html
                            {/* /build */}
                            <div className="well well-sm text-center">{t('login_with')}</div>
                            {/* build:include ../../../views/_forms/login_socials.html */}
                            This will be replaced by the content of description.html
                            {/* /build */}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RegisterComponent;