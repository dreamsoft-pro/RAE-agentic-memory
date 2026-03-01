import api from "@/lib/api";

class DeliveryWidgetService {
    static async reducePostData(data: any): Promise<any> {
        // Implement the logic for reducing postData here.
        return data;  // Placeholder, replace with actual implementation
    }
}

const newItem = {};
let scope = {};  // Ensure this is properly initialized elsewhere in your code

if (scope.selectedTechnology) {
    newItem['selectedTechnology'] = scope.selectedTechnology;
}

const rIdx = -1;  // Example initialization, use the correct value from your context
if (rIdx > -1) {
    if (
        scope.realisationTimes[rIdx]?.overwriteDate !== undefined &&
        scope.realisationTimes[rIdx].overwriteDate !== null
    ) {
        newItem['realizationDate'] = scope.realisationTimes[rIdx].overwriteDate;
    } else {
        newItem['realizationDate'] = scope.realisationTimes[rIdx]?.date ?? new Date();  // Default value example, adjust as needed
    }
}

(async () => {
    const productAddresses = await DeliveryWidgetService.reducePostData(scope.productAddresses);
    newItem['productAddresses'] = productAddresses;

    if (scope.calculation) {
        newItem['weight'] = scope.calculation.weight;
    }

    const $rootScope = {};  // Ensure this is properly initialized elsewhere in your code
    newItem['currency'] = $rootScope.currentCurrency?.code ?? 'default_currency';  // Default value example, adjust as needed
})();