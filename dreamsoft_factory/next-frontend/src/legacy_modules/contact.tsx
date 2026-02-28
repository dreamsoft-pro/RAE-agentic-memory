/**
 * Service: contact
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';
import { Container, Row, Col } from 'reactstrap';

const ContactPage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <Container id="content-contact">
      <Row>
        <Col md={12}>
          <h1 className="page-header">{t('contact')}</h1>
          <Row>
            <Col md={3}>
              <div className="staticContentBox" data-content="static.contact"></div>
            </Col>
            <Col md={9}>
              <div ui-view="contact-form"></div>
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  );
};

export default ContactPage;