import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class AuthService {
    private API_URL = process.env.NEXT_PUBLIC_API_URL;

    public async login(username: string, password: string): Promise<boolean> {
        try {
            const response = await axios.post(`${this.API_URL}/login`, {
                username,
                password
            });

            if (response.status === 200) {
                // Assume you have some mechanism to handle success, e.g., setting logged status.
                return true;
            } else {
                throw new Error('Unexpected response');
            }
        } catch (error: any) {
            if (error.response && error.response.status === 400) {
                console.error('wrong_mail_password'); // Replace with proper Notification mechanism
            } else {
                console.error(`Error ${error.message}`);
            }
            return false;
        }
    }

    public updateProductAddress(product: { addresses: any[] }) {
        DeliveryWidgetService.reducePostData(product.addresses).then((productAddresses) => {
            // Handle the promise resolution here.
        }).catch((err) => {
            console.error('Error updating product address:', err);
        });
    }
}

// Example usage:
const authService = new AuthService();
authService.login('user@example.com', 'password123').then(loggedIn => {
    if (loggedIn) {
        // User logged in successfully
    } else {
        // Handle login failure
    }
});

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    const authService = new AuthService();
    return authService.login(req.body.username, req.body.password).then(loggedIn => {
        if (loggedIn) {
            res.status(200).json({ success: true });
        } else {
            res.status(401).json({ error: 'Login failed' });
        }
    }).catch(() => {
        res.status(500).json({ error: 'Internal server error' });
    });
}