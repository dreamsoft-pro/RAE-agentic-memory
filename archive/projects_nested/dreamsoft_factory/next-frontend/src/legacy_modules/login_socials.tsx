/**
 * Service: login_socials
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const LoginSocials: React.FC = () => {
    const loginGoogle = () => {
        // Your login logic for Google
        console.log('Login with Google');
    };

    const loginFacebook = () => {
        // Your login logic for Facebook
        console.log('Login with Facebook');
    };

    return (
        <ul className="list-unstyled list-social">
            <li>
                <a 
                    href="#" 
                    onClick={loginGoogle} 
                    className="btn btn-block btn-social btn-lg btn-google"
                >
                    <span className="fa fa-google"></span>
                    Sign in with Google
                </a>
            </li>
            <li>
                <a 
                    href="#" 
                    onClick={loginFacebook} 
                    className="btn btn-block btn-social btn-lg btn-facebook"
                >
                    <span className="fa fa-facebook"></span>
                    Sign in with Facebook
                </a>
            </li>
        </ul>
    );
};

export default LoginSocials;