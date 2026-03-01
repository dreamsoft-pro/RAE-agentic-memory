/**
 * Service: client-zone-change-pass
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface ChangePasswordFormProps {
    form: {
        oldPass: string;
        pass: string;
        confirmPass: string;
    };
    change: () => void;
}

const ChangePasswordForm: React.FC<ChangePasswordFormProps> = ({ form, change }) => (
    <div className="panel panel-default">
        <div className="panel-heading">
            <h2 className="panel-title">{'change_password' | translate}</h2>
        </div>
        <div className="panel-body">
            <form onSubmit={change} className="form-horizontal" role="form">
                <div className="form-group">
                    <label htmlFor="user-old-password" className="col-md-3 control-label">{'current_password' | translate}</label>
                    <div className="col-md-9">
                        <input 
                            type="password" 
                            className="form-control" 
                            value={form.oldPass} 
                            onChange={(e) => form.oldPass = e.target.value} 
                            placeholder={'current_password' | translate} 
                            required 
                            id="user-old-password"
                        />
                    </div>
                </div>
                <div className="form-group">
                    <label htmlFor="user-password" className="col-md-3 control-label">{'password' | translate}</label>
                    <div className="col-md-9">
                        <input 
                            type="password" 
                            className="form-control" 
                            value={form.pass} 
                            onChange={(e) => form.pass = e.target.value} 
                            placeholder={'password' | translate} 
                            required 
                            id="user-password"
                        />
                    </div>
                </div>
                <div className="form-group">
                    <label htmlFor="user-password-repeat" className="col-md-3 control-label">{'repeat_password' | translate}</label>
                    <div className="col-md-9">
                        <input 
                            type="password" 
                            className="form-control" 
                            value={form.confirmPass} 
                            onChange={(e) => form.confirmPass = e.target.value} 
                            placeholder={'repeat_password' | translate} 
                            required 
                            id="user-password-repeat"
                        />
                    </div>
                </div>
                <div className="form-group">
                    <div className="col-md-3 col-md-offset-9">
                        <button type="submit" className="btn btn-success btn-block btn-submit">{'save' | translate}</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
);

export default ChangePasswordForm;