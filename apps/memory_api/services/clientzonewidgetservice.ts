javascript
function acceptReport(product, file, $scope) {
    ProductFileService.acceptReport(product.productID, file.ID).then(responseHandler);

    function responseHandler(response) {
        if (response.response) {
            // [BACKEND_ADVICE] Handle report and product acceptance
            handleAcceptanceResponse(response, file.name, $scope);
        } else {
            Notification.info($filter('translate')('error'));
        }
    }

    function handleAcceptanceResponse(response, fileName, scope) {
        if (response.reportAccepted) {
            Notification.info($filter('translate')('report_accepted') + ' ' + fileName);
        }
        if (response.productAccepted) {
            Notification.info($filter('translate')('product_accepted'));
        }
        scope.getNextPage(scope.pagingSettings.currentPage);
    }
}
