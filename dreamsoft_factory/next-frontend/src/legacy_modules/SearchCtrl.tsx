/**
 * Service: SearchCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

/**
 */
import React from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { withRouter, RouteComponentProps } from 'react-router-dom';
import { NotificationService, PsTypeService, PhotoFolderService } from './services';
import _ from 'lodash';

interface SearchCtrlProps extends RouteComponentProps<{ text?: string }> {
    $rootScope: any;
    ctx: any;
    $state: any;
    $filter: any;
    Notification: any;
    PsTypeService: any;
    $stateParams: { text?: string };
}

const SearchCtrl: React.FC<SearchCtrlProps> = ({ $stateParams, ctx, $rootScope, PhotoFolderService, $state }) => {
    const searchText = $stateParams.text;
    ctx.results = [];
    ctx.searchText = searchText;

    const init = () => {
        PsTypeService.search(searchText).then((data: any) => {
            ctx.results = data;
        });
    };

    React.useEffect(() => {
        init();
    }, []);

    return null; // This is a dummy return since the component logic is moved to useEffect and hooks
};

const mapStateToProps = (state: any) => ({
    // Map state here if needed
});

const mapDispatchToProps = (dispatch: any) => bindActionCreators({
    // Define action creators here if needed
}, dispatch);

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(SearchCtrl));