javascript
import { addAddress, saveAddressToSession } from '@/lib/api';
import { success as notifySuccess } from '@/utils/notifications';

const countries = []; // Assuming countries is defined elsewhere

let form = {};

function addAddressForm() {
    form.saving = true;
    form.type = 1;

    return addAddress(form).then(data => {
        if (data.response === true) {
            form = {};
            form.saving = false;
            addresses.push(data.item);
            return saveAddressToSession(data.addressID).then(sessionData => {
                if (sessionData.response) {
                    notifySuccess('saved');
                }
            });
        }
    });
}

// [BACKEND_ADVICE] Consider moving heavy logic to backend services.
