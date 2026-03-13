/**
 * Service: password-remind
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

const PasswordRemind: React.FC = () => {
  const [email, setEmail] = useState('');
  const { t } = useTranslation();

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    // Handle form submission logic here
  };

  return (
    <div className="container" id="content-remind-password">
      <div className="row">
        <div className="col-xs-12">
          <h1 className="page-header">{t('password_remind')}</h1>
          <p>{t('newpass_text')}</p>
          <form onSubmit={handleSubmit} method="post" className="form-horizontal">
            <div className="form-group">
              <label htmlFor="user-email" className="col-sm-2 control-label">
                {t('email')}
              </label>
              <div className="col-sm-10">
                <input
                  onKeyUp={event => event.keyCode === 13 && handleEmail()}
                  autoComplete="on"
                  placeholder={t('email')}
                  name="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  id="user-email"
                  className="form-control"
                  type="email"
                />
              </div>
            </div>
            <div className="form-group">
              <div className="col-md-10 col-sm-offset-2">
                <button data-toggle="submit" type="submit" className="btn btn-success btn-submit">
                  {t('send')}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default PasswordRemind;