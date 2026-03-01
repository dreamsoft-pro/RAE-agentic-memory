import { useEffect, useState } from 'react';
import axios from 'axios';

interface CartItem {
    _id: number;
}

interface Credentials {
    carts?: number[];
    user?: any;
}

const LoginComponent = () => {
    const [credentials, setCredentials] = useState<Credentials>({});
    const [onetime, setOnetime] = useState<boolean>(false);

    useEffect(() => {
        // Assuming oneCart is obtained from some state or props
        const oneCart: CartItem = { _id: 123 }; // Example cart item

        if (!credentials.carts) {
            credentials.carts = [];
        }
        credentials.carts.push(oneCart._id);

        login(credentials).then(data => {
            handleLoginSuccess(data);
        });
    }, [onetime]);

    const login = async (creds: Credentials): Promise<Credentials> => {
        try {
            // Assuming AuthService.login is a function that returns a promise
            return await axios.post('/api/login', creds); // Replace with actual API endpoint
        } catch (error) {
            throw error;
        }
    };

    const handleLoginSuccess = async (data: Credentials) => {
        console.log('Logged in successfully');
        
        if (data.user && data.user.super) {
            alert('login_success'); // Use your preferred way to show success message
        }

        await getDefaultAddress();
    };

    const getDefaultAddress = async () => {
        try {
            // Assuming DpAddressService.getDefaultAddress is a function that returns a promise
            const response = await axios.get('/api/address/default', { params: { id: 1 } }); // Replace with actual API endpoint
            
            if (response.data.response) {
                console.log('Default address retrieved successfully');
                
                await getAllAddresses();
            }
        } catch (error) {
            throw error;
        }
    };

    const getAllAddresses = async () => {
        try {
            // Assuming getAddress is a function that returns a promise
            const allAddressResponse = await axios.get('/api/address/all'); // Replace with actual API endpoint
            
            console.log('All addresses retrieved successfully');
        } catch (error) {
            throw error;
        }
    };

    return (
        <div>
            {/* Your component JSX goes here */}
        </div>
    );
};

export default LoginComponent;