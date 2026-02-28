/**
 * Service: footer-links
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const FooterLinks: React.FC = () => {
    return (
        <div className="container">
            <div className="row">
                <div className="col-md-4">
                    <div className="well well-small">
                        <legend>
                            <span>{'newsletter_group' | translate}</span>
                        </legend>
                        <p>{'sign_up_for_newsletter' | translate}</p>
                        <form className="form-inline">
                            <label className="sr-only">{'newsletter_group' | translate}</label>
                            <div className="input-group clearfix">
                                <div className="input-group-addon bg-success"><i className="fa fa-envelope"></i></div>
                                <input type="text" className="form-control" placeholder={'email' | translate} />
                            </div>
                            <br />
                            <button type="submit" className="btn btn-sm btn-muted voffset2">{'sign_up' | translate}</button>
                        </form>
                    </div>
                </div>
                <div className="col-md-8">
                    <form className="form-inline">
                        <a href="#" className="havent_found_product_img"></a>
                    </form>
                </div>
                <div className="col-md-12">
                    <div className="well">
                        <div className="row">
                            <div className="col-md-2">
                                <ul className="text-left nav nav-stacked text-center">
                                    <li><a href={uiSref('login')}>{'login' | translate}</a></li>
                                    <li><a href={uiSref('statute')}>{'statute' | translate}</a></li>
                                    <li><a href={uiSref('help')}>{'help' | translate}</a></li>
                                    <li><a href={uiSref('contact')}>{'contact' | translate}</a></li>
                                    <li><a href={uiSref('client-zone-send-reclamation')}>{'send_reclamation' | translate}</a></li>
                                </ul>
                            </div>
                            <div className="col-md-2">
                                <ul className="text-left nav nav-stacked text-center">
                                    <li><a href={uiSref('client-zone-affiliate-program')}>{'collect_points' | translate}</a></li>
                                    <li><a href={uiSref('statute')}>{'statute' | translate}</a></li>
                                    <li><a href={uiSref('help')}>{'help' | translate}</a></li>
                                    <li><a href={uiSref('contact')}>{'contact' | translate}</a></li>
                                    <li><a href={uiSref('client-zone-send-reclamation')}>{'send_reclamation' | translate}</a></li>
                                </ul>
                            </div>
                            <div className="col-md-2">
                                <ul className="text-left nav nav-stacked text-center">
                                    <li><a href={uiSref('client-zone-affiliate-program')}>{'collect_points' | translate}</a></li>
                                    <li><a href={uiSref('statute')}>{'statute' | translate}</a></li>
                                    <li><a href={uiSref('help')}>{'help' | translate}</a></li>
                                    <li><a href={uiSref('contact')}>{'contact' | translate}</a></li>
                                    <li><a href={uiSref('client-zone-send-reclamation')}>{'send_reclamation' | translate}</a></li>
                                </ul>
                            </div>
                            <div className="col-md-2">
                                <ul className="text-left nav nav-stacked text-center">
                                    <li><a href={uiSref('client-zone-affiliate-program')}>{'collect_points' | translate}</a></li>
                                    <li><a href={uiSref('statute')}>{'statute' | translate}</a></li>
                                    <li><a href={uiSref('help')}>{'help' | translate}</a></li>
                                    <li><a href={uiSref('contact')}>{'contact' | translate}</a></li>
                                    <li><a href={uiSref('client-zone-send-reclamation')}>{'send_reclamation' | translate}</a></li>
                                </ul>
                            </div>
                            <div className="col-md-2">
                                <ul className="text-left nav nav-stacked text-center">
                                    <li><a href={uiSref('client-zone-affiliate-program')}>{'collect_points' | translate}</a></li>
                                    <li><a href={uiSref('statute')}>{'statute' | translate}</a></li>
                                    <li><a href={uiSref('help')}>{'help' | translate}</a></li>
                                    <li><a href={uiSref('contact')}>{'contact' | translate}</a></li>
                                    <li><a href={uiSref('client-zone-send-reclamation')}>{'send_reclamation' | translate}</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FooterLinks;