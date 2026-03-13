/**
 * Service: footer-news
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom'; // Assuming you are using react-router for navigation

const NewsFooter: React.FC = () => {
    const { t, i18n } = useTranslation();

    return (
        <div className="container" id="news">
            <div className="row">
                <div className="col-md-12">
                    <div className="page-header">
                        <h2 className="text-muted">{t('informations')}</h2>
                    </div>
                </div>
                <div className="col-md-4">
                    <h3>Lorem ipsum dolor sit amet</h3>
                    <p>Curabitur volutpat luctus sapien, mattis tempor leo pulvinar et. Vivamus pellentesque sodales mauris, eu volutpat diam blandit ac. Aliquam erat volutpat. Duis et sapien magna, in vulputate felis. Etiam placerat venenatis urna sodales aliquet. Praesent facilisis tortor sed enim commodo interdum.</p>
                    <button as={Link} to="index-news" className="btn btn-sm btn-default">{t('read_more')}</button>
                </div>
                <div className="col-md-4">
                    <h3>Lorem ipsum dolor sit amet</h3>
                    <p>Curabitur volutpat luctus sapien, mattis tempor leo pulvinar et. Vivamus pellentesque sodales mauris, eu volutpat diam blandit ac. Aliquam erat volutpat. Duis et sapien magna, in vulputate felis. Etiam placerat venenatis urna sodales aliquet. Praesent facilisis tortor sed enim commodo interdum.</p>
                    <p>Morbi malesuada, metus vitae imperdiet facilisis, lectus ante porttitor neque, nec pharetra nulla est vestibulum nisi. Quisque rutrum vulputate dolor, sit amet luctus leo auctor ac. Nullam sit amet erat a justo egestas imperdiet. Curabitur euismod dui vitae velit dapibus congue. Vestibulum sed risus eu nisi viverra blandit. Phasellus in ante eget diam fermentum sodales.</p>
                    <button as={Link} to="index-news" className="btn btn-sm btn-default">{t('read_more')}</button>
                </div>
                <div className="col-md-4">
                    <h3>Lorem ipsum dolor sit amet</h3>
                    <p>Curabitur volutpat luctus sapien, mattis tempor leo pulvinar et. Vivamus pellentesque sodales mauris, eu volutpat diam blandit ac. Aliquam erat volutpat. Duis et sapien magna, in vulputate felis. Etiam placerat venenatis urna sodales aliquet. Praesent facilisis tortor sed enim commodo interdum.</p>
                    <p>Morbi malesuada, metus vitae imperdiet facilisis, lectus ante porttitor neque, nec pharetra nulla est vestibulum nisi. Quisque rutrum vulputate dolor, sit amet luctus leo auctor ac. Nullam sit amet erat a justo egestas imperdiet. Curabitur euismod dui vitae velit dapibus congue. Vestibulum sed risus eu nisi viverra blandit. Phasellus in ante eget diam fermentum sodales.</p>
                    <button as={Link} to="index-news" className="btn btn-sm btn-default">{t('read_more')}</button>
                </div>
            </div>
        </div>
    );
};

export default NewsFooter;