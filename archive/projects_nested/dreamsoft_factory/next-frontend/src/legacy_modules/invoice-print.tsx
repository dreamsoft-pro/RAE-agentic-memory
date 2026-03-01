/**
 * Service: invoice-print
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import styled from 'styled-components';

// Styled components for the styles defined in the original CSS
const Container = styled.div`
  width: 50%;
  font-size: 12em;
`;

const Header = styled.div``;

const Logo = styled.div`
  display: inline;
  width: 33%;
  img {
    width: 33%;
    height: auto;
  }
`;

const Middle = styled.div`
  display: inline;
  width: 33%;
`;

const CreateDate = styled.div`
  display: inline;
  width: 31%;
  text-align: right;
`;

const Clear = styled.div`
  clear: both;
`;

const Title = styled.div`
  margin-top: 15px;
  h2 {
    text-align: center;
  }
`;

const Products = styled.div`
  margin: 0 1%;
  .table {
    width: 80%;
    font-size: 11px;
  }
`;

interface ProductRowProps {
  isEven: boolean;
}

const ProductRow = styled.tr<ProductRowProps>`
  padding: 3px;
  background: ${props => (props.isEven ? '#F1F3FA' : '#FFFFFF')};
`;

interface InvoicePrintProps {
  // Define props here if needed
}

const InvoicePrint: React.FC<InvoicePrintProps> = () => {
  return (
    <Container>
      <Header>
        <Logo className="logo">
          <img src="path_to_image" alt="Logo" />
        </Logo>
        <Middle className="middle"></Middle>
        <CreateDate className="createDate"></CreateDate>
        <Clear className="clear"></Clear>
      </Header>
      <Title className="title">
        <h2>Invoice Title</h2>
      </Title>
      <Products className="products">
        <table className="table">
          <thead>
            <tr className="productHead">
              <th>Product Details</th>
            </tr>
          </thead>
          <tbody>
            <ProductRow isEven={false}></ProductRow>
            {/* Add more rows dynamically if needed */}
          </tbody>
        </table>
      </Products>
    </Container>
  );
};

export default InvoicePrint;