/**
 * Service: MainCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState, useRef } from 'react';
import { useDispatch, useSelector, useStore } from 'react-redux';
import { useHistory, useLocation } from 'react-router-dom';
import { MainWidgetService, MenuTypesService, DpCartsDataService } from './services';
import _ from 'lodash';

const MainCtrl: React.FC = () => {
    const [menuShow, setMenuShow] = useState(false);
    const [actualFile, setActualFile] = useState<string[]>([]);
    const dispatch = useDispatch();
    const store = useStore();
    const history = useHistory();
    const location = useLocation();
    const rootScope = useSelector((state: any) => state.rootScope);

    useEffect(() => {
        MainWidgetService.includeTemplateVariables({}, 'header');
        MainWidgetService.getMegaMenu().then(megaMenu => {
            if (megaMenu.items.length > 0) {
                megaMenu.items[0].isVisible = true;
            }
            rootScope.menuItems = megaMenu.items;
            if (megaMenu.visible === 1) {
                rootScope.showMenu = true;
            } else {
                rootScope.showMenu = false;
            }
            rootScope.menuType = megaMenu.menuType;
            if (!rootScope.menuType) {
                rootScope.menuType = 1;
            }
            rootScope.allTypes = MenuTypesService.getAllTypes(megaMenu.items);
        });

        MainWidgetService.getForms().then(forms => {
            rootScope.forms = forms;
        });

        const handleResize = () => {
            if (window.innerWidth < 768) {
                document.querySelectorAll('.navbar-collapse li a.navbarLink').forEach(el => {
                    el.setAttribute('data-toggle', 'collapse');
                    el.setAttribute('data-target', '#navbar');
                });
            } else {
                document.querySelectorAll('.navbar-collapse li a.navbarLink').forEach(el => {
                    el.removeAttribute('data-toggle');
                    el.removeAttribute('data-target');
                });
            }
        };

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    useEffect(() => {
        if (rootScope.logged) {
            DpCartsDataService.get(rootScope.user.userID).then(result => {
                if (result[0]) {
                    rootScope.orderID = result[0].orderID;
                }
                store.dispatch({ type: 'cartRequired' });
            });
        }
    }, [rootScope.logged]);

    useEffect(() => {
        const intervalHandler = setInterval(() => {
            if ($('.navbar-collapse li a.navbarLink').length > 0) {
                if (window.innerWidth < 768) {
                    document.querySelectorAll('.navbar-collapse li a.navbarLink').forEach(el => {
                        el.setAttribute('data-toggle', 'collapse');
                        el.setAttribute('data-target', '#navbar');
                    });
                } else {
                    document.querySelectorAll('.navbar-collapse li a.navbarLink').forEach(el => {
                        el.removeAttribute('data-toggle');
                        el.removeAttribute('data-target');
                    });
                }
            }
        }, 500);

        return () => clearInterval(intervalHandler);
    }, []);

    const toggleMenu = () => setMenuShow(!menuShow);

    const checkState = (stateName: string) => $rootScope.current.state === stateName;

    const scrollToTop = () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleZoomStaticImage = (urls: string[]) => {
        if (!Array.isArray(urls)) {
            urls = [urls];
        }
        setActualFile(urls);
    };

    return (
        <div>
            {/* Your component JSX here */}
        </div>
    );
};

export default MainCtrl;