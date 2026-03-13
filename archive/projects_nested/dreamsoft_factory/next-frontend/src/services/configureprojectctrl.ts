javascript
import '@/lib/api';
import FormatService from './services/format-service';
import PagesService from './services/pages-service';
import AttributeService from './services/attribute-service';

Promise.all([
    FormatService.getPublic($scope.complexID),
    PagesService.getPublic(),
    AttributeService.getFullOptions()
]).then(data => {
    newProduct.formats = data[0];

    const attributesData = data[2];
    if (attributesData.length === 0) {
        emptyProducts++;
    }

    if (emptyProducts === countGroups) {
        $scope.emptyProduct = true;
    }

    const customFormatIndex = _.findIndex(attributesData, { attrID: -1 });
    if (customFormatIndex > -1) {
        newProduct.customFormatInfo = attributesData[customFormatIndex];
        // [BACKEND_ADVICE] Consider the logic for splicing the array here.
        attributesData.splice(customFormatIndex, 1);
    }
});
