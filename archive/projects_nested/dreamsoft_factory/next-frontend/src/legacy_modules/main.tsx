/**
 * Service: main
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { render } from 'react-dom';
import { Router, Route, Switch } from 'react-router-dom';
import { createBrowserHistory } from 'history';
import Header from './components/Header';
import Content from './components/Content';
import Footer from './components/Footer';

const history = createBrowserHistory();

const App: React.FC = () => (
  <Router history={history}>
    <>
      <Header />
      <Switch>
        <Route path="/" component={Content} />
      </Switch>
      <Footer />
    </>
  </Router>
);

render(<App />, document.getElementById('root'));
