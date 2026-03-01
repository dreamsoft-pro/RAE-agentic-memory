javascript
if (delivery !== undefined) {
    const isExcluded = _.indexOf(excluded, delivery.ID) === -1;

    if (isExcluded) {
        address.deliveries.push(delivery);
    } else {
        const filteredIndex = _.findIndex(address.deliveries, { ID: delivery.ID });

        // [BACKEND_ADVICE] Heavy logic to remove and update the delivery
        if (filteredIndex > -1) {
            address.deliveries.splice(filteredIndex, 1);

            if (address.deliveryID === delivery.ID) {
                selectedExcluded = true;
            }
        }
    }
}

if (selectedExcluded) {
    address.deliveryID = _.first(address.deliveries)?.ID ?? '';
}
