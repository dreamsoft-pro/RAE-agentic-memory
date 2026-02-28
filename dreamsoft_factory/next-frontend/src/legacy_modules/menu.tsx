/**
 * Service: menu
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useSelector } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';

const Menu = () => {
    const navigate = useNavigate();
    const { categoryurl, groupid, typeid } = useParams();
    const currentLang = useSelector((state: RootState) => state.language);
    const menuItems = useSelector((state: RootState) => state.menu.items);

    return (
        <div className="panel panel-default panel-menu" id="panel-product-menu">
            <div className="panel-heading">
                <h3 className="panel-title">Menu</h3>
            </div>
            <div className="panel-body">
                <ul className="nav nav-pills nav-stacked left-menu" id="product-menu">
                    {menuItems.map((item, key) => (
                        <li key={key}>
                            <a href="#" id={`category-${item.ID}`} data-target={`#submenu-${key}`} data-toggle="collapse" data-parent="#product-menu">
                                {item.langs[currentLang.code].name}
                                {item.types.length + item.childs.length + item.groups.length > 0 ? (
                                    <span className="pull-right fa fa-fw fa-plus" />
                                ) : (
                                    <span className="pull-right fa fa-fw fa-minus" />
                                )}
                            </a>
                            <ul id={`submenu-${key}`} className="nav nav-stacked collapse">
                                {item.types.length > 0 && item.types.map((type) => (
                                    <li key={type.ID}>
                                        <a href="#" onClick={() => navigate(`calculate/${categoryurl}/${groupid}/${type.ID}`)} className="el-type">
                                            {type.names[currentLang.code]}
                                        </a>
                                    </li>
                                ))}
                                {item.childs.length > 0 && item.childs.map((child) => (
                                    <li key={child.ID}>
                                        <a href="#" onClick={() => navigate(`category/${child.langs[currentLang.code].url}`)} className="el-child">
                                            {child.langs[currentLang.code].name}
                                            {child.types.length > 0 ? (
                                                <span className="pull-right fa fa-fw fa-plus fa-sm" />
                                            ) : (
                                                <span className="pull-right fa fa-fw fa-minus fa-sm" />
                                            )}
                                        </a>
                                        {child.types.length > 0 || child.groups.length > 0 ? (
                                            <ul className="nav nav-stacked">
                                                {child.types.length > 0 && child.types.map((type) => (
                                                    <li key={type.ID}>
                                                        <a href="#" onClick={() => navigate(`calculate/${categoryurl}/${groupid}/${type.ID}`)} className="el-type">
                                                            {type.names[currentLang.code]}
                                                        </a>
                                                    </li>
                                                ))}
                                                {child.groups.length > 0 && child.groups.map((group) => (
                                                    <li key={group.ID}>
                                                        <a href="#" onClick={() => navigate(`group/${categoryurl}/${group.ID}`)} className="el-group">
                                                            {group.names[currentLang.code]}
                                                        </a>
                                                        {group.types.length > 0 && (
                                                            <ul className="nav nav-stacked">
                                                                {group.types.map((type) => (
                                                                    <li key={type.ID}>
                                                                        <a href="#" onClick={() => navigate(`calculate/${categoryurl}/${group.ID}/${type.ID}`)} className="el-type">
                                                                            {type.names[currentLang.code]}
                                                                        </a>
                                                                    </li>
                                                                ))}
                                                            </ul>
                                                        )}
                                                    </li>
                                                ))}
                                            </ul>
                                        ) : null}
                                    </li>
                                ))}
                            </ul>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default Menu;