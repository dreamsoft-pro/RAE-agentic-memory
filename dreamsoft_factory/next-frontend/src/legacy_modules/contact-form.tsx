/**
 * Service: contact-form
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface ContactFormProps {
    mailSent: boolean;
    sendMessage: (formName: string) => void;
    contactForm: {
        userName: string;
        subject: string;
        email: string;
        content: string;
    };
}

const ContactForm: React.FC<ContactFormProps> = ({ mailSent, sendMessage, contactForm }) => {
    return (
        <div className="form">
            <form onSubmit={() => sendMessage('form1')} className="form-horizontal ng-pristine ng-valid" noValidate>
                <h3 className="text-right">{'fill_form_to_contact' | translate}</h3>

                <div className="form-group">
                    <label className="col-md-6 control-label">{'name_and_lastname' | translate}</label>
                    <div className="col-md-6">
                        <input 
                            type="text" 
                            value={contactForm.userName} 
                            onChange={(e) => contactForm.userName = e.target.value} 
                            name="name" 
                            placeholder={'name_and_lastname' | translate} 
                            required 
                            className="form-control" 
                        />
                    </div>
                </div>

                <div className="form-group">
                    <label className="col-md-6 control-label">{'subject' | translate}</label>
                    <div className="col-md-6">
                        <input 
                            type="text" 
                            value={contactForm.subject} 
                            onChange={(e) => contactForm.subject = e.target.value} 
                            name="subject" 
                            placeholder={'subject' | translate} 
                            required 
                            className="form-control" 
                        />
                    </div>
                </div>

                <div className="form-group">
                    <label className="col-md-6 control-label">{'email' | translate}</label>
                    <div className="col-md-6">
                        <div className="input-group">
                            <span className="input-group-addon">
                                <i className="fa fa-envelope"></i>
                            </span>
                            <input 
                                type="email" 
                                value={contactForm.email} 
                                onChange={(e) => contactForm.email = e.target.value} 
                                name="email" 
                                placeholder={'email' | translate} 
                                required 
                                className="form-control" 
                            />
                        </div>
                    </div>
                </div>

                <div className="form-group">
                    <label className="col-md-6 control-label">{'content' | translate}</label>
                    <div className="col-md-6">
                        <textarea 
                            value={contactForm.content} 
                            onChange={(e) => contactForm.content = e.target.value} 
                            placeholder={'content' | translate} 
                            required 
                            className="form-control" 
                        />
                    </div>
                </div>

                <div className="form-group">
                    <div className="col-md-offset-6 col-md-6">
                        {/* Assuming vc-recaptcha is a custom component or library */}
                        <vc-recaptcha 
                            theme="light" 
                            key={contactForm.key} // Adjust based on your logic for the key
                            onSuccess={(response) => setResponse(response)}
                            onExpire={cbExpiration}
                        />
                    </div>
                </div>

                <div className="form-group">
                    <div className="col-md-4 col-md-offset-8">
                        <button type="submit" className="btn btn-success btn-lg btn-block">
                            <i className="fa fa-check"></i> {'send' | translate}
                        </button>
                    </div>
                </div>
            </form>

            {mailSent && (
                <div className="alert alert-success">{'thank_you_for_sent_message' | translate}</div>
            )}
        </div>
    );
};

export default ContactForm;