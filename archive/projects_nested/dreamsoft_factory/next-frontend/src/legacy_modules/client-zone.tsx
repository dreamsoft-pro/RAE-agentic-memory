/**
 * Service: client-zone
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link, NavLink } from 'react-router-dom';

const ClientZone: React.FC = () => {
    const { t } = useTranslation();

    return (
        <div className="container" id="content-client-zone">
            <div className="row continue-shopping">
                <div className="col-md-12 col-sm-12">
                    <div className="well well-sm">
                        <Link to="/home" className="btn btn-default btn-block">{t('continue_shopping')}</Link>
                    </div>
                </div>
            </div>

            <a onClick={() => changeSearchType('advanced')} className="regular-link">
                <span className="small">{t('advanced_search')}</span>
            </a>

            <hr />

            <h5>{t('my_account')}</h5>
            <ul className="nav nav-pills nav-stacked">
                {menuBottom.map((item, index) => (
                    <li key={index} className={currentState === item.name ? 'active' : ''}>
                        <NavLink to={`/${item.name}`}>
                            <i className={`fa fa-fw ${1==1?'fa-truck':''}`}></i> {item.ncyBreadcrumb.label}
                        </NavLink>
                    </li>
                ))}
            </ul>

            {showQuota && (
                <div className="panel panel-default">
                    <div className="panel-heading">
                        <h2 className="panel-title">{t('quota')}</h2>
                    </div>
                    <div className="panel-body">
                        {t('user')}: STANDARD<br />
                        {t('available_space')}: {usedSpace}Mb/1Tb
                    </div>
                </div>
            )}

            <div className="row">
                <div className="col-xs-12">
                    <h1 className="page-header">{t('myzone')}</h1>
                </div>
            </div>

            <nav className="navbar navbar-default navbar-myzone" role="navigation">
                <div className="navbar-header visible-xs">
                    <button type="button" className="navbar-toggle" data-toggle="collapse" data-target="#client-zone-nav">
                        <span className="sr-only">Toggle navigation</span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                    </button>
                    <div className="navbar-brand">
                        {t('orders')}
                    </div>
                </div>
                <div className="collapse navbar-collapse" id="client-zone-nav">
                    <ul className="nav nav-pills nav-stacked">
                        {menuTop.map((item, index) => (
                            <li key={index} className={currentState === item.name ? 'active' : ''}>
                                <NavLink to={`/${item.name}`}>
                                    <i className="fa fa-fw fa-table"></i> {item.ncyBreadcrumb.label}
                                </NavLink>
                            </li>
                        ))}
                    </ul>
                    <hr />
                    <form name="searchSimple" onSubmit={search} role="search">
                        {(companyID === 35 || companyID === 25 || companyID === 195) ? (
                            <div className="input-group">
                                <input type="text" className="form-control" value={tag} onChange={(e) => setTag(e.target.value)} placeholder="tag" />
                                <span className="input-group-btn">
                                    <button type="submit" className="btn btn-primary btn-search">
                                        <span className="fa fa-search"></span>
                                    </button>
                                </span>
                            </div>
                        ) : (
                            <div className="input-group">
                                <input type="text" className="form-control" value={order} onChange={(e) => setOrder(e.target.value)} placeholder={t('No_or_name_of_the_order')} />
                                <span className="input-group-btn">
                                    <button type="submit" className="btn btn-primary btn-search">
                                        <span className="fa fa-search"></span>
                                    </button>
                                </span>
                            </div>
                        )}
                    </form>

                    <form name="searchAdvanced" onSubmit={search} role="search">
                        <div className="input-group">
                            <input type="text" className="form-control" value={author} onChange={(e) => setAuthor(e.target.value)} placeholder={t('author')} />
                            <span className="input-group-btn">
                                <button type="submit" className="btn btn-primary btn-search">
                                    <span className="fa fa-search"></span>
                                </button>
                            </span>
                        </div>
                        <div className="input-group">
                            <input type="text" className="form-control" value={place} onChange={(e) => setPlace(e.target.value)} placeholder={t('place')} />
                            <span className="input-group-btn">
                                <button type="submit" className="btn btn-primary btn-search">
                                    <span className="fa fa-search"></span>
                                </button>
                            </span>
                        </div>
                        <div className="input-group">
                            <input type="text" className="form-control" value={person} onChange={(e) => setPerson(e.target.value)} placeholder={t('person')} />
                            <span className="input-group-btn">
                                <button type="submit" className="btn btn-primary btn-search">
                                    <span className="fa fa-search"></span>
                                </button>
                            </span>
                        </div>
                    </form>
                </div>
            </nav>
        </div>
    );
};

export default ClientZone;