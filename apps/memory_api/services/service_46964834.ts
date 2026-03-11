import api from '@/lib/api';
import _ from 'lodash';

export default class ProductProcessor {
    async processProduct(product: any, savedProduct: any): Promise<void> {
        savedProduct.productAddresses = [];
        let volumeSum = 0;
        let actualVolume = 0;

        _.each(product.addresses, (oneAddress, index) => {
            const newAddressItem: any = {};
            volumeSum += oneAddress.volume;
            newAddressItem.deliveryID = oneAddress.deliveryID;
            newAddressItem.volume = oneAddress.volume;
            newAddressItem.allVolume = oneAddress.allVolume;
            newAddressItem.senderID = oneAddress.senderID;
            newAddressItem.addressID = oneAddress.addressID;
            newAddressItem.commonDeliveryID = oneAddress.commonDeliveryID;
            newAddressItem.commonRealisationTime = oneAddress.commonRealisationTime;
            newAddressItem.join = oneAddress.join !== undefined ? oneAddress.join : false;

            if (savedProduct.newVolumesProductAddresses && savedProduct.newVolumesProductAddresses[index] > 0) {
                newAddressItem.volume = newAddressItem.allVolume = savedProduct.newVolumesProductAddresses[index];
            }

            savedProduct.productAddresses.push(newAddressItem);

            // Assuming `def.resolve(savedProduct);` is part of an async context, we'll handle it differently.
            if (index === product.addresses.length - 1) {
                return Promise.resolve(savedProduct);
            }
        });

        // Since the method returns a promise, ensure the last operation resolves properly
        return Promise.resolve();
    }
}