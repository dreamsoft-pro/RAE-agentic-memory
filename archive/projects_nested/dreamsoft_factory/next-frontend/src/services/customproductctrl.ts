javascript
import { api } from '@/lib/api';

// [BACKEND_ADVICE] Add logic to handle tab activation.
setTimeout(() => {
    document.querySelector('.with-nav-tabs .nav-tabs li').classList.add('active');
    document.querySelector('.with-nav-tabs .tab-content div.tab-pane').classList.add('active');
}, 300);

$scope.formatSizeUnits = function (bytes) {
    return api.formatSizeUnits(bytes);
};

$scope.removeFile = function(fileItem) {
    fileItem.remove();
};

// [BACKEND_ADVICE] This method should be evaluated for backend handling.
$scope.hasFormats = function (desc) {
    return true;
};

// [BACKEND_ADvice] This method should be evaluated for backend handling.
$scope.hasOneFormat = function (pattern) {
    return true;
};

$scope.login = function (credentials) {
    const backTo = {
        state: 'custom-product',
        params: {
            categoryurl: $state.params.categoryurl,
            groupurl: $state.params.groupurl,
            typeurl: $state.params.typeurl
        }
    };
    api.login(credentials, backTo);
};
