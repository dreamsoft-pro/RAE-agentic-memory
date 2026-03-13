import { useState, useEffect } from 'react';
import axios from 'axios';

type Address = {
    senderID: string;
    addressID: string;
};

type DefaultAddress = {
    address: { ID: string };
};

interface AuthService {
    updateDefaultAddress(params: { addressID: string }): Promise<void>;
}

const ProductComponent = () => {
    const [address, setAddress] = useState<Address>({ senderID: '', addressID: '' });
    const [defaultAddress, setDefaultAddress] = useState<DefaultAddress | null>(null);

    useEffect(() => {
        if (allAddress && allAddress.senders.length) {
            setAddress((prevAddr) => ({
                ...prevAddr,
                senderID: allAddress.senders[0].type
            }));
        }

        if (defaultAddress && defaultAddress.address.ID) {
            setAddress((prevAddr) => ({
                ...prevAddr,
                addressID: defaultAddress.address.ID
            }));

            updateProductAddress(product);
        }
    }, [allAddress, defaultAddress]);

    const handleUpdateDefaultAddress = async () => {
        try {
            await AuthService.updateDefaultAddress({ addressID: defaultAddress?.address.ID ?? '' });
            def.resolve(true);

            if (onetime) {
                Notification.success('you_can_order_now');
            } else {
                Notification.success('login_success');
            }
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            {/* Your component JSX */}
        </div>
    );
};

// Assuming the following are defined elsewhere in your codebase
const allAddress: { senders: Array<{ type: string }> };
const product: any;
const AuthService: AuthService;

export default ProductComponent;