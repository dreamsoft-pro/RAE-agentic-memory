/**
 * Service: news
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { format, parseISO } from 'date-fns';

interface ArticleProps {
    article: {
        timestamp: string;
        comments: string;
        title: string;
        description: string;
        link: string;
    };
}

const NewsArticle: React.FC<ArticleProps> = ({ article }) => {
    const formattedDate = format(parseISO(article.timestamp), 'yyyy-MM-dd HH:mm');

    return (
        <div className="container" id="footer-news">
            <div className="row">
                <div className="col-md-12">
                    <div className="portlet light blueHoki">
                        <div className="portlet-title">
                            <div className="caption">
                                <i className="fa fa-shopping-cart"></i> {/* Assuming 'newses' is translated, replace with actual translation function */}
                            </div>
                            <div className="tools"></div>
                        </div>
                        <div className="portlet-body">
                            <div className="col-md-12 blog-tag-data">
                                <div className="archive-item voffsetBottom5">
                                    <div className="row news-divide">
                                        <div className="col-md-12">
                                            <p className="archive-top-date">
                                                <small>
                                                    <span className="date">{formattedDate}</span>
                                                    <span className="month"></span>
                                                    <a target="_blank" href={article.comments} className="comments pull-right">
                                                        <i className="fa fa-comments"></i> {/* Assuming 'comments' is translated, replace with actual translation */}
                                                        Comments
                                                    </a>
                                                </small>
                                            </p>
                                            <h3>{article.title}</h3>
                                            <p>{article.description}</p>
                                            <a target="_blank" href={article.link} className="btn btn-sm btn-primary pull-left">
                                                {/* Assuming 'read_more' is translated, replace with actual translation */}
                                                Read More
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default NewsArticle;