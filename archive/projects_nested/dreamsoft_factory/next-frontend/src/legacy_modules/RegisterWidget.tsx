/**
 * Service: RegisterWidget
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

/**
 */
import _ from 'lodash';
import { $filter, $rootScope } from 'angular';

interface Country {
    code: string;
    areaCode?: string;
}

interface Scope {
    form: {
        ad_countryCode: string;
        del_countryCode: string;
        fv_countryCode: string;
        ad_areaCode?: string;
        del_areaCode?: string;
    };
    noRegisterForm: {
        ad_countryCode: string;
        fv_countryCode: string;
        ad_areaCode?: string;
        del_areaCode?: string;
    };
    countries: Country[];
}

interface RegisterWidget {
    initCodeRegister: (scope: Scope, countries: Country[]) => void;
    initCodeWithoutRegister: (scope: Scope, countries: Country[]) => void;
    selectCountryRegister: (scope: Scope, prefix: string) => void;
    selectCountryWithoutRegister: (scope: Scope, prefix: string) => void;
    findFormAreaCode: (scope: Scope, formName: string, code: string, oldVal: string) => void;
}

const RegisterWidget: RegisterWidget = (( $rootScope, $filter ) => {
    const initCodeRegister = (scope: Scope, countries: Country[]) => {
        const upCode = $filter('uppercase')($rootScope.currentLang.code);
        scope.form.ad_countryCode = upCode;
        scope.form.del_countryCode = upCode;
        scope.form.fv_countryCode = upCode;

        const idx = _.findIndex(countries, { code: upCode });
        if (idx > -1) {
            if (countries[idx].areaCode !== undefined) {
                scope.form.ad_areaCode = countries[idx].areaCode;
                scope.form.del_areaCode = countries[idx].areaCode;
            }
        }
    };

    const initCodeWithoutRegister = (scope: Scope, countries: Country[]) => {
        const upCode = $filter('uppercase')($rootScope.currentLang.code);
        scope.noRegisterForm.ad_countryCode = upCode;
        scope.noRegisterForm.fv_countryCode = upCode;

        const idx = _.findIndex(countries, { code: upCode });
        if (idx > -1) {
            if (countries[idx].areaCode !== undefined) {
                scope.noRegisterForm.ad_areaCode = countries[idx].areaCode;
            }
        }
    };

    const selectCountryRegister = (scope: Scope, prefix: string) => {
        const code = scope.form[`${prefix}_countryCode`];
        const idx = _.findIndex(scope.countries, { code });
        if (idx > -1) {
            if (scope.countries[idx].areaCode !== undefined) {
                scope.form[`${prefix}_areaCode`] = scope.countries[idx].areaCode;
            } else {
                scope.form[`${prefix}_areaCode`] = '';
            }
        }
    };

    const selectCountryWithoutRegister = (scope: Scope, prefix: string) => {
        const code = scope.noRegisterForm[`${prefix}_countryCode`];
        const idx = _.findIndex(scope.countries, { code });
        if (idx > -1) {
            if (scope.countries[idx].areaCode !== undefined) {
                scope.noRegisterForm[`${prefix}_areaCode`] = scope.countries[idx].areaCode;
            } else {
                scope.noRegisterForm[`${prefix}_areaCode`] = '';
            }
        }
    };

    const findFormAreaCode = (scope: Scope, formName: string, code: string, oldVal: string) => {
        if (code !== oldVal) {
            const idx = _.findIndex(scope.countries, { code });
            if (idx > -1) {
                if (scope.countries[idx].areaCode !== undefined) {
                    scope[formName].areaCode = scope.countries[idx].areaCode;
                } else {
                    scope[formName].areaCode = '';
                }
            }
        }
    };

    return {
        initCodeRegister,
        initCodeWithoutRegister,
        selectCountryRegister,
        selectCountryWithoutRegister,
        findFormAreaCode
    };
})( $rootScope, $filter );

export default RegisterWidget;