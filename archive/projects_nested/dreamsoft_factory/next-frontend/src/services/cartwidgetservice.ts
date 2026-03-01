javascript
let tmpDeliveryPrice;

if ($scope.productAddresses !== undefined) {
    for (let i = 0; i < $scope.productAddresses.length; i++) {
        tmpDeliveryPrice = 0;

        const tmp_price = $scope.productAddresses[i].price.toString();
        tmpDeliveryPrice += parseFloat(tmp_price.replace(',', '.'));

        price += Number(tmpDeliveryPrice);

        // [BACKEND_ADVICE] Handle undefined scenarios gracefully.
        if ($scope.calculation.volume !== undefined) {
            net_per_pcs = price / $scope.calculation.volume;
        }
    }
}
