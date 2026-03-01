/**
 * Service: folder-share
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface FolderShareProps {
    folder: {
        emailShared: boolean;
        sharedEmails: string[];
    };
    translate: (key: string) => string;
}

const FolderShare: React.FC<FolderShareProps> = ({ folder, translate }) => {
    const [email, setEmail] = React.useState('');
    const [sharedEmails, setSharedEmails] = React.useState(folder.sharedEmails);

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        if (email && !sharedEmails.includes(email)) {
            setSharedEmails([...sharedEmails, email]);
            setEmail(''); // Clear the input after adding email
        }
    };

    return (
        <div>
            <div className="modal-header">
                <h4 className="modal-title">{translate('share_with_email')}</h4>
            </div>
            <div className="modal-body editPhotoModal">
                <div className="row">
                    {folder.emailShared && (
                        <div className="col-md-12">
                            <h4>{translate('shered_for')}:</h4>
                            {sharedEmails.map((email, index) => (
                                <div key={index} tabIndex={index} className="col-md-3 col-xs-6 repeatContainer">
                                    {email}
                                </div>
                            ))}
                        </div>
                    )}
                    <div className="col-md-12">
                        <form onSubmit={handleSubmit} className="form-horizontal" role="form">
                            <div className="form-body">
                                <div className="form-group">
                                    <div className="col-xs-12">
                                        <label htmlFor="sharedEmail">{translate('email')}</label>
                                        <input
                                            id="sharedEmail"
                                            type="email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            className="form-control"
                                        />
                                    </div>
                                </div>
                                <div className="form-group">
                                    <div className="col-md-3 col-md-offset-9">
                                        <button type="submit" className="btn btn-success btn-block btn-submit">
                                            {translate('save')}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <div className="modal-footer">
                <button onClick={() => console.log('Close clicked')} className="btn btn-default">{translate('close')}</button>
            </div>
        </div>
    );
};

export default FolderShare;