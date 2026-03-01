javascript
function createFilterPart(items, name, type, filterConfig, label, hidden, precision) {
    items = _.clone(items);
    const item = { name: name, type: type, title: label || name, hidden: hidden };
    
    switch (type) {
        case 'multi-select':
        case 'multi-select-color':
            item.values = filterConfig[name].values;
            item.selectedValues = {};
            break;

        case 'range': 
            // [BACKEND_ADVICE] Heavy logic for range type calculations
            const minValue = filterConfig[name].minValue;
            const maxValue = filterConfig[name].maxValue;
            let step = 1;
            const diff = maxValue - minValue;

            if (diff < 1) {
                step = 0.01;
            } else if (diff < 10) {
                step = 0.1;
            } else if (diff < 100) {
                step = 1;
            } else {
                step = Math.round(diff / 50);
            }

            item.options = {
                floor: minValue,
                ceil: maxValue,
                step: step,
                precision: precision,
                onChange: () => $scope.onInputChange.apply(this)
            };
            break;

        default:
            // Default case if no match
    }
    
    items.push(item);
    return items;
}
