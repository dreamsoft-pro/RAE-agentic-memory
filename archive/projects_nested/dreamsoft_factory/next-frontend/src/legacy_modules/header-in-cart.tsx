/**
 * Service: header-in-cart
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';
import logoPlaceholder from '../../assets/logo_placeholder.png'; // Adjust the import according to your asset management

const HeaderInCart: React.FC = () => {
    const { t, i18n } = useTranslation();
    const location = useLocation();
    const companyID = 'yourCompanyID';
    const domainID = 'yourDomainID';

    const languages = [
        { code: 'en', name: 'English', active: true },
        { code: 'es', name: 'Spanish', active: false },
        // Add more languages as needed
    ];

    const switchLanguage = (code: string, isActive: boolean) => {
        if (!isActive) {
            i18n.changeLanguage(code);
        }
    };

    const currentLang = languages.find((lang) => lang.active);

    return (
        <nav className="navbar navbar-default navbar-fixed-top navbar-minimal">
            <div className="container">
                <div className="navbar-header">
                    <Link to="/" title={t('home')} className="navbar-brand">
                        <img src={`${process.env.STATIC_URL}uploadedFiles/${companyID}/logos/${domainID}/logo` || logoPlaceholder} loading="lazy" alt={t('home')} />
                    </Link>
                </div>
                <wcga />
            </div>
            <div>
                <a href="#" title={t('change_language')} className="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false" id="langMenu">
                    <span className="visible-xs-inline visible-lg-inline">{currentLang?.name}</span>
                    <i className="fa fa-globe visible-xs-inline visible-sm-inline visible-md-inline"></i>
                    <span className="caret"></span>
                </a>
                <ul className="dropdown-menu dropdown-menu-right" role="menu">
                    {languages.map((lang) => (
                        <li key={lang.code}>
                            <a href="" onClick={(e) => { e.preventDefault(); switchLanguage(lang.code, lang.active); }}>
                                {lang.name}
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
            <div className="container">
                <div className="row">
                    <div className="col-xs-12">
                        <div data-cy="breadcrumb">{location.pathname !== '/' && <ncyBreadcrumb />}</div>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default HeaderInCart;