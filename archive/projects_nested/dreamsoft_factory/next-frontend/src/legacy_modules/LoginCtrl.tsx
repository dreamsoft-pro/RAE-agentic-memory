/**
 * Service: LoginCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import * as React from 'react';
import { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { useDispatch, useSelector } from 'react-redux';
import { useHistory, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { login, checkAuth, getUser, passForget, changeMail, loginFacebook, loginGoogle } from './actions';

interface LoginCtrlProps {
    // Define props here if needed
}

const LoginCtrl: React.FC<LoginCtrlProps> = ({ /*props*/ }) => {
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const dispatch = useDispatch();
    const history = useHistory();
    const location = useLocation();
    const { t } = useTranslation();

    useEffect(() => {
        dispatch(checkAuth());
    }, [dispatch]);

    const handleLogin = () => {
        dispatch(login(credentials, history.location.state || {}));
    };

    const handleCheck = () => {
        dispatch(checkAuth()).then((data) => {
            if (data) setLogged(true);
            else setLogged(false);
        });
    };

    const handleGetUser = () => {
        return dispatch(getUser());
    };

    const handlePassForget = () => {
        dispatch(passForget({ email: 'example@example.com' })).then(() => {
            console.log('Email sent successfully');
        }).catch((error) => {
            console.log('Failed to send email', error);
        });
    };

    const handleChangeMail = () => {
        dispatch(changeMail({ form: {} })).then(() => {
            console.log('Email changed successfully');
        }).catch((error) => {
            console.log('Failed to change email', error);
        });
    };

    const handleLoginFacebook = () => {
        dispatch(loginFacebook());
    };

    const handleLoginGoogle = () => {
        dispatch(loginGoogle());
    };

    // State management for logged in status
    const [logged, setLogged] = useState(false);

    return (
        <div>
            <h1>{t('login.title')}</h1>
            <input type="text" placeholder={t('username')} onChange={(e) => setCredentials({ ...credentials, username: e.target.value })} />
            <input type="password" placeholder={t('password')} onChange={(e) => setCredentials({ ...credentials, password: e.target.value })} />
            <button onClick={handleLogin}>{t('login')}</button>
            <button onClick={handleCheck}>{t('checkAuth')}</button>
            <button onClick={handleGetUser}>{t('getUser')}</button>
            <button onClick={handlePassForget}>{t('passForget')}</button>
            <button onClick={handleChangeMail}>{t('changeMail')}</button>
            <button onClick={handleLoginFacebook}>{t('loginFacebook')}</button>
            <button onClick={handleLoginGoogle}>{t('loginGoogle')}</button>
        </div>
    );
};

export default connect()(LoginCtrl);