/**
 * Service: search
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you are using react-router-dom for navigation

interface ItemProps {
    item: any;
    currentLang: any;
    companyID: string;
}

const SearchItem: React.FC<ItemProps> = ({ item, currentLang, companyID }) => {
    const STATIC_URL = process.env.STATIC_URL || ''; // Assuming you have environment variables set up for this

    return (
        <div className="col-xs-6 col-sm-4 col-md-3">
            <div className="thumbnail clearfix" style={{ display: 'flex', flexDirection: 'column' }}>
                {item.isEditor && !item.isCustomProduct ? (
                    <Link to={`select-project/${item.langs[currentLang.code].url}/${item.group.slugs[currentLang.code]}/${item.slugs[currentLang.code]}`} className="thumbnail-link">
                        {!item.icons[currentLang.code] && !item.icon ? (
                            <img loading="lazy" src={`${STATIC_URL}${companyID}/images/productholder.png`} alt="" className="img-responsive" />
                        ) : (
                            <img loading="lazy" src={item.icon.url} alt="" className="img-responsive" />
                        )}
                    </Link>
                ) : item.isCustomProduct ? (
                    <Link to={`custom-product/${item.langs[currentLang.code].url}/${item.group.slugs[currentLang.code]}/${item.slugs[currentLang.code]}`} className="thumbnail-link">
                        {item.icon ? (
                            <img loading="lazy" src={item.icon.url} alt="" className="img-responsive" />
                        ) : (
                            <img loading="lazy" src={`${STATIC_URL}${companyID}/images/productholder.png`} alt="" className="img-responsive" />
                        )}
                    </Link>
                ) : (
                    <Link to={`calculate/${item.category.langs[currentLang.code].url}/${item.group.slugs[currentLang.code]}/${item.slugs[currentLang.code]}`} className="thumbnail-link">
                        {!item.icons[currentLang.code] && !item.icon ? (
                            <img loading="lazy" src={`${STATIC_URL}${companyID}/images/productholder.png`} alt="" className="img-responsive" />
                        ) : (
                            <img loading="lazy" src={item.icon.url} alt="" className="img-responsive" />
                        )}
                    </Link>
                )}
                <div className="caption">
                    <h3>
                        {item.isEditor && !item.isCustomProduct ? (
                            <Link to={`select-project/${item.langs[currentLang.code].url}/${item.group.slugs[currentLang.code]}/${item.slugs[currentLang.code]}`}>
                                {item.names[currentLang.code]}
                            </Link>
                        ) : item.isCustomProduct ? (
                            <Link to={`custom-product/${item.langs[currentLang.code].url}/${item.group.slugs[currentLang.code]}/${item.slugs[currentLang.code]}`}>
                                {item.names[currentLang.code]}
                            </Link>
                        ) : (
                            <Link to={`calculate/${item.category.langs[currentLang.code].url}/${item.group.slugs[currentLang.code]}/${item.slugs[currentLang.code]}`}>
                                {item.names[currentLang.code]}
                            </Link>
                        )}
                    </h3>
                    <div className="description" dangerouslySetInnerHTML={{ __html: item.icons[currentLang.code] }}></div>
                </div>
                {item.isEditor && !item.isCustomProduct ? (
                    <Link to={`select-project/${item.langs[currentLang.code].url}/${item.group.slugs[currentLang.code]}/${item.slugs[currentLang.code]}`} className="btn btn-block btn-info btn-flat btn-more">
                        {/* Translations can be handled via a translation function */}
                        Show More
                    </Link>
                ) : item.isCustomProduct ? (
                    <Link to={`custom-product/${item.langs[currentLang.code].url}/${item.group.slugs[currentLang.code]}/${item.slugs[currentLang.code]}`} className="btn btn-block btn-info btn-flat btn-more">
                        {/* Translations can be handled via a translation function */}
                        Show More
                    </Link>
                ) : (
                    <Link to={`calculate/${item.category.langs[currentLang.code].url}/${item.group.slugs[currentLang.code]}/${item.slugs[currentLang.code]}`} className="btn btn-block btn-info btn-flat btn-more">
                        {/* Translations can be handled via a translation function */}
                        Show More
                    </Link>
                )}
            </div>
        </div>
    );
};

export default SearchItem;