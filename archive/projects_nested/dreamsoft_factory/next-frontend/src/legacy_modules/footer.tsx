/**
 * Service: footer
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';
import LazyLoad from 'react-lazyload';

interface Article {
  timestamp: string;
  image: string;
  title: string;
  shortDescription?: string;
  description?: string;
  link: string;
}

const Footer = ({ articles, showArticles }) => {
  const { t } = useTranslation();

  if (!showArticles || articles.length === 0) return null;

  return (
    <div className="container news">
      <div className="row">
        {[...Array(4)].map((_, index) => (
          <div key={index} className="col-md-3 blog-tag-data">
            {articles.slice(0, 4).map((article: Article, idx) => (
              <div key={idx} className="archive-item voffsetBottom5">
                <div className="row news-divide">
                  <div className="col-md-12">
                    <p className="archive-top-date">
                      <small>
                        <span className="date">{new Date(article.timestamp).toISOString().split('T')[0]}</span>
                        <span className="month"></span>
                      </small>
                    </p>
                    {article.image && (
                      <div className="image">
                        <LazyLoad height={150} offset={[-150, 0]}>
                          <img loading="lazy" alt="" src={article.image} />
                        </LazyLoad>
                      </div>
                    )}
                    <h3>{article.title}</h3>
                    {article.shortDescription ? (
                      <p className="short-text-article">{article.shortDescription}</p>
                    ) : (
                      <p className="short-text-article">{article.description}</p>
                    )}
                    <a target="_blank" href={article.link} className="btn btn-sm btn-primary pull-left">
                      {t('read_more')}
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Footer;