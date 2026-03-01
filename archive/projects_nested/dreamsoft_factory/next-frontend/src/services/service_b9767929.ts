import { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

class AuthController {
    async login(req: NextApiRequest, res: NextApiResponse) {
        // Your logic for login
    }

    async loginInCart(req: NextApiRequest, res: NextApiResponse) {
        // Your logic for login in cart
    }
}

export default (req: NextApiRequest, res: NextApiResponse) => {
    const authController = new AuthController();

    if (req.method === 'POST' && req.query.action === 'login') {
        return authController.login(req, res);
    }

    if (req.method === 'POST' && req.query.action === 'loginInCart') {
        return authController.loginInCart(req, res);
    }

    res.status(405).json({ message: 'Method Not Allowed' });
};