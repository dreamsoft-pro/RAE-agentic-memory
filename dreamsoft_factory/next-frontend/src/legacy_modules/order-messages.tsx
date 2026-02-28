/**
 * Service: order-messages
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Message {
    user?: { name: string, lastname: string };
    content: string;
    created: string;
    read: number;
    isAdmin: boolean;
}

interface Props {
    typeOfResource: string;
    order: { ID: string };
    messages: Message[];
    send: () => void;
    form: { message: string };
}

const OrderMessages: React.FC<Props> = ({ typeOfResource, order, messages, send, form }) => {
    return (
        <div className="modal-header">
            <h4 className="modal-title">
                {typeOfResource === 'order' ? `${'order_messages' | translate} - ${order.ID}` : `${'offer_messages' | translate} - ${order.ID}`}
            </h4>
        </div>
    );
};

const OrderMessagesTable: React.FC<Props> = ({ messages }) => {
    return (
        <div className="modal-body orderMsgContent">
            <div className="row">
                <div className="col-md-12">
                    <table className="table">
                        <thead>
                            <tr>
                                <th style={{ width: '25%' }}>{'author' | translate}</th>
                                <th>{'content' | translate}</th>
                                <th>{'date' | translate}</th>
                            </tr>
                        </thead>
                        <tbody>
                            {messages.map((message, index) => (
                                <tr key={index}>
                                    <td className="author">
                                        {message.user ? `${message.user.name} ${message.user.lastname}` : <b>{'print_house' | translate}</b>}
                                    </td>
                                    <td className="content">
                                        {message.content}
                                        {message.read === 0 && message.isAdmin && <i className="fa fa-clock-o" title={"'unread_message' | translate"}></i>}
                                    </td>
                                    <td style={{ width: '20%' }} className="date">{message.created}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

const OrderMessagesForm: React.FC<Props> = ({ send, form }) => {
    return (
        <form className="form-horizontal" role="form" onSubmit={send} data-toggle="validator">
            <div className="form-group">
                <div className="col-sm-12">
                    <textarea required ngMinlength="3" ngModel={form.message} className="form-control" placeholder={'content' | translate}>
                    </textarea>
                </div>
            </div>
            <div className="form-group">
                <div className="col-md-4">
                    <button type="submit" className="btn btn-success btn-block btn-submit">{'send' | translate}</button>
                </div>
            </div>
        </form>
    );
};

const OrderMessagesFooter: React.FC<Props> = ({ $dismiss }) => {
    return (
        <div className="modal-footer">
            <button className="btn btn-default" onClick={$dismiss}>{'close' | translate}</button>
        </div>
    );
};

const OrderMessagesComponent: React.FC<Props> = ({ typeOfResource, order, messages, send, form }) => {
    return (
        <div>
            <OrderMessages typeOfResource={typeOfResource} order={order} />
            <OrderMessagesTable messages={messages} />
            <OrderMessagesForm form={form} send={send} />
            <OrderMessagesFooter $dismiss={$dismiss} />
        </div>
    );
};