/**
 * Service: _login
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

const LoginComponent: React.FC = () => {
    const { t } = useTranslation();

    return (
        <div className="container" id="content-login">
            <div className="row">
                <div className="col-xs-12">
                    <h1 className="page-header">{t('login_or_register')}</h1>
                </div>
            </div>
            <div className="row">
                <div className="col-md-6">
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            <h3 className="panel-title">{t('log_in')}</h3>
                        </div>
                        <div className="panel-body">
                            {/* build:include ../../../views/_forms/login.html */}
                            This will be replaced by the content of description.html
                            {/* /build */}
                        </div>
                    </div>
                </div>
                <div className="col-md-6">
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            <h3 className="panel-title">{t('register')}</h3>
                        </div>
                        <div className="panel-body">
                            <p>
                                <span>{t('do_not_have_account')}</span>
                                <a href="#register" data-tooltip="">{t('register')}</a>!
                            </p>
                            <h3>{t('login_with')}</h3>
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

export default LoginComponent;