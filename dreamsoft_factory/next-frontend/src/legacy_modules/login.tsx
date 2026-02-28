/**
 * Service: login
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

interface Credentials {
    email: string;
    password: string;
}

const LoginForm: React.FC = () => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const [credentials, setCredentials] = useState<Credentials>({ email: '', password: '' });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setCredentials({ ...credentials, [name]: value });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Here you would typically dispatch an action to log in the user
        console.log('Logging in with:', credentials);
        navigate('/dashboard'); // Assuming successful login navigates to dashboard
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.keyCode === 13) {
            handleSubmit(e);
        }
    };

    return (
        <form className="form-horizontal" onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="user-email" className="col-md-4 control-label">{t('login')}</label>
                <div className="col-md-8">
                    <input 
                        onChange={handleInputChange}
                        onKeyUp={handleKeyPress}
                        className="form-control" 
                        type="text" 
                        placeholder={t('login')} 
                        name="email" 
                        value={credentials.email} 
                        required 
                        id="user-email" 
                    />
                </div>
            </div>
            <div className="form-group">
                <label htmlFor="user-password" className="col-md-4 control-label">{t('password')}</label>
                <div className="col-md-8">
                    <input 
                        onChange={handleInputChange}
                        onKeyUp={handleKeyPress}
                        className="form-control" 
                        type="password" 
                        placeholder={t('password')} 
                        name="password" 
                        value={credentials.password} 
                        required 
                        id="user-password" 
                    />
                </div>
            </div>
            <div className="form-group">
                <div className="col-md-offset-4 col-md-8">
                    <button type="submit" className="btn btn-success btn-block btn-submit btn-login">
                        {t('log_in')}
                    </button>
                    <hr />
                    <span>{t('did_you_forget_your_password')}</span>
                    <a href="#/password-remind" data-toggle="tooltip">{t('password_remind')}</a>
                </div>
            </div>
        </form>
    );
};

export default LoginForm;