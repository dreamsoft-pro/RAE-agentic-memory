javascript
import { BackendService } from '@/lib/api';
import { UppercaseFilter, CurrentLanguageService } from '@/services';

export const RegisterWidgetFactory = (BackendService) => {
    function initCodeRegister(scope, countries) {
        // [BACKEND_ADVICE] Consider moving country code lookup to backend service for efficiency.
        const upCode = new UppercaseFilter(CurrentLanguageService.currentLang.code);

        scope.form.ad_countryCode = upCode;
        scope.form.del_countryCode = upCode;
        scope.form.fv_countryCode = upCode;

        const idx = countries.findIndex(country => country.code === upCode);

        if (idx !== -1 && countries[idx].areaCode !== undefined) {
            scope.form.ad_areaCode = countries[idx].areaCode;
            scope.form.del_areaCode = countries[idx].areaCode;
        }
    }

    function initCodeWithoutRegister(scope, countries) {
        const upCode = new UppercaseFilter(CurrentLanguageService.currentLang.code);

        scope.noRegisterForm.ad_countryCode = upCode;
        scope.noRegisterForm.fv_countryCode = upCode;
    }

    return {
        initCodeRegister,
        initCodeWithoutRegister
    };
};

BackendService.register(RegisterWidgetFactory);
