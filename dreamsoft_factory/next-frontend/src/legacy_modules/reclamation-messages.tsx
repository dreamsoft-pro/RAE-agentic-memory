/**
 * Service: reclamation-messages
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faClockO } from '@fortawesome/free-regular-svg-icons';
import Tooltip from 'react-tooltip'; // Assuming you have a tooltip library

interface Message {
    user: { name: string, lastname: string };
    content: string;
    created: string;
    read: number;
    isAdmin: boolean;
}

interface ReclamationMessagesProps {
    reclamation: { ID: string },
    messages: Message[]
}

const ReclamationMessages: React.FC<ReclamationMessagesProps> = ({ reclamation, messages }) => {
    const { t } = useTranslation();
    const [formData, setFormData] = React.useState({ message: '' });

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Handle form submission logic here
    };

    return (
        <div>
            <div className="modal-header">
                <h4 className="modal-title">{t('reclamation_messages')} - {reclamation.ID}</h4>
            </div>
            <div className="modal-body reclamationMsgContent">
                <div className="row">
                    <div className="col-md-12">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th style={{ width: '25%' }}>{t('author')}</th>
                                    <th>{t('content')}</th>
                                    <th>{t('date')}</th>
                                </tr>
                            </thead>
                            <tbody>
                                {messages.map((message, index) => (
                                    <tr key={index}>
                                        <td className="author">
                                            {message.user ? `${message.user.name} ${message.user.lastname}` : <b>{t('print_house')}</b>}
                                        </td>
                                        <td className="content">
                                            {message.content}
                                            {!message.read && message.isAdmin && (
                                                <FontAwesomeIcon icon={faClockO} data-tip={t('unread_message')} />
                                            )}
                                            <Tooltip place="top" effect="solid" />
                                        </td>
                                        <td style={{ width: '20%' }} className="date">{message.created}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        <form onSubmit={handleSubmit} data-toggle="validator">
                            <div className="form-group">
                                <div className="col-sm-12">
                                    <textarea required name="message" value={formData.message} onChange={handleChange} placeholder={t('content')} className="form-control"></textarea>
                                </div>
                            </div>
                            <div className="form-group">
                                <div className="col-md-4">
                                    <button type="submit" className="btn btn-success btn-block">{t('send')}</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <div className="modal-footer">
                <button onClick={() => { /* close logic */ }} className="btn btn-default">{t('close')}</button>
            </div>
        </div>
    );
};

export default ReclamationMessages;