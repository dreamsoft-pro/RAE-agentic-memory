/**
 * Service: select-project
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

interface Item {
    _id: string;
    name: string;
    url?: string;
}

interface Props {
    type: {
        names: Record<string, string>;
        category: {
            langs: Record<string, { url: string }>;
        };
        group: {
            slugs: Record<string, string>;
        };
        slugs: Record<string, string>;
    };
    mainThemes: Item[];
    companyID: string;
    STATIC_URL: string;
}

const SelectProject: React.FC<Props> = ({ type, mainThemes, companyID, STATIC_URL }) => {
    const { currentLang } = useTranslation();

    return (
        <div className="container" id="content-select-project">
            <div className="row">
                <div className="col-md-12">
                    <h1 className="page-header main-page-header">{type.names[currentLang.code]}</h1>
                </div>
            </div>
            <div className="row row-products-list">
                <div className="col-xs-12">
                    <div className="row">
                        {mainThemes.map((item, index) => (
                            <div key={index} className="col-xs-6 col-sm-4 col-md-3">
                                <div className="thumbnail clearfix">
                                    {item.url ? (
                                        <Link to={{
                                            pathname: `/configure-project`,
                                            state: {
                                                categoryurl: type.category.langs[currentLang.code].url,
                                                groupurl: type.group.slugs[currentLang.code],
                                                typeurl: type.slugs[currentLang.code],
                                                mainthemeid: item._id
                                            }
                                        }} className="thumbnail-link">
                                            <img loading="lazy" src={`${STATIC_URL}${companyID}/images/productholder.png`} alt="" className="img-responsive" />
                                        </Link>
                                    ) : (
                                        <Link to={{
                                            pathname: `/configure-project`,
                                            state: {
                                                categoryurl: type.category.langs[currentLang.code].url,
                                                groupurl: type.group.slugs[currentLang.code],
                                                typeurl: type.slugs[currentLang.code],
                                                mainthemeid: item._id
                                            }
                                        }} className="thumbnail-link">
                                            <img loading="lazy" src={`${STATIC_URL}editor${item.url}`} alt="" className="img-responsive" />
                                        </Link>
                                    )}
                                    <div className="caption">
                                        <h3>
                                            <Link to={{
                                                pathname: `/configure-project`,
                                                state: {
                                                    categoryurl: type.category.langs[currentLang.code].url,
                                                    groupurl: type.group.slugs[currentLang.code],
                                                    typeurl: type.slugs[currentLang.code],
                                                    mainthemeid: item._id
                                                }
                                            }}>
                                                {item.name}
                                            </Link>
                                        </h3>
                                        <div className="description" dangerouslySetInnerHTML={{ __html: item.name }}></div>
                                    </div>
                                    <Link to={{
                                        pathname: `/configure-project`,
                                        state: {
                                            categoryurl: type.category.langs[currentLang.code].url,
                                            groupurl: type.group.slugs[currentLang.code],
                                            typeurl: type.slugs[currentLang.code],
                                            mainthemeid: item._id
                                        }
                                    }} className="btn btn-block btn-info btn-flat btn-more">
                                        {t('show_more')}
                                    </Link>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SelectProject;