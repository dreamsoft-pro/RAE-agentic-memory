import api from "@/lib/api";
import _ from "lodash";

class ProductHandler {
    async handleProductSelection(selectedProduct: any, scope: any): Promise<void> {
        let newItem = {};
        let rIdx: number;

        if (selectedProduct !== null) {
            newItem.groupID = selectedProduct.groupID ?? scope.currentGroupID;
            newItem.typeID = selectedProduct.typeID ?? scope.currentTypeID;
            newItem.taxID = selectedProduct.taxID ?? scope.productItem.taxID;
            newItem.name = selectedProduct.name ?? scope.productItem.name;
            newItem.realizationTimeID = selectedProduct.realizationTimeID ?? scope.productItem.realisationTime;
            newItem.productAddresses = selectedProduct.addresses ?? [];
            rIdx = _.findIndex(scope.realisationTimes, { ID: newItem.realizationTimeID });
        } else {
            newItem.groupID = scope.currentGroupID;
            newItem.typeID = scope.currentTypeID;
            newItem.taxID = scope.productItem.taxID;
            newItem.name = scope.productItem.name;
            newItem.realizationTimeID = scope.productItem.realisationTime;
            rIdx = _.findIndex(scope.realisationTimes, { ID: newItem.realizationTimeID });
        }

        // Further logic with newItem and rIdx can be added here
    }
}