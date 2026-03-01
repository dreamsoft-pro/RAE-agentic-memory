/**
 * Service: shared-project
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

const ShareProject: React.FC<{ source?: string }> = ({ source }) => {
    const { t } = useTranslation();
    const [form, setForm] = React.useState({ email: '' });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.id]: e.target.value });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Assuming send() is a function that sends the email
        console.log('Sending email:', form.email);
    };

    return (
        <div className="container" id="share-project">
            <div className="row">
                <div className="col-md-12">
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            <h2 className="panel-title">{t('project')}</h2>
                        </div>
                        <div className="panel-body">
                            {source === 'email' && (
                                <div className="row">
                                    <div className="col-md-12 text-center">
                                        <form onSubmit={handleSubmit} className="form" role="form">
                                            <div className="form-body">
                                                <div className="form-group">
                                                    <div className="col-md-6 col-md-offset-3">
                                                        <label htmlFor="projectEmail">{t('password')}</label>
                                                        <input 
                                                            id="projectEmail" 
                                                            onChange={handleChange} 
                                                            value={form.email} 
                                                            type="email" 
                                                            className="form-control" 
                                                        />
                                                    </div>
                                                </div>
                                                <div className="form-group">
                                                    <div className="col-md-6 col-md-offset-3">
                                                        <button 
                                                            type="submit" 
                                                            className="btn btn-success btn-block btn-submit"
                                                        >
                                                            {t('send')}
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            )}
                            {source === 'facebook' && (
                                <div className="row">
                                    <div className="col-md-12">
                                        <div className="col-md-6 col-md-offset-3">
                                            <button 
                                                onClick={() => console.log('Opening project on Facebook')} 
                                                className="btn btn-block btn-lg btn-success"
                                            >
                                                {t('open_project')}
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ShareProject;