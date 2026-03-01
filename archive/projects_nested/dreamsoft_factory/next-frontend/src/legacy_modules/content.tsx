/**
 * Service: content
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import styled from 'styled-components';

const StyledDiv = styled.div`
  .stickyStyle1 {
    position: sticky;
    top: 60px;
  }
`;

const LeftMenuProductsList = styled.ul`
  list-style: none;
`;

const LeftMenuProductItem = styled.li`
  width: 100%;
  padding-left: 15px;
  font-size: 14px !important;
`;

const LeftMenuLink = styled.a`
  padding-top: 10px !important;
  padding-bottom: 10px !important;
`;

const LeftMenuItemsList = styled.ul`
  list-style: none;
`;

const LeftMenuItem = styled.li`
  width: 100%;
  padding-left: 15px;
  font-size: 12px !important;
`;

const LeftMenuItemsLink = styled.a`
  padding-top: 5px !important;
  padding-bottom: 5px !important;
`;

const PanelRightOrderMax = styled.div`
  overflow: hidden;
`;

const MediaQuery932 = styled.div`
  @media (max-width: 932px) {
    .owfh {
      overflow: hidden;
    }
  }
`;

const ContentComponent: React.FC<{ product: any }> = ({ product }) => {
  return (
    <StyledDiv className="thumbnail relType4 clearfix" ng-if={product.relType == 2 && !product.isEditor && product.isCustomProduct}>
      <LeftMenuProductsList>
        <LeftMenuProductItem>
          <LeftMenuLink href="#">Product Link</LeftMenuLink>
        </LeftMenuProductItem>
      </LeftMenuProductsList>
      <LeftMenuItemsList>
        <LeftMenuItem>
          <LeftMenuItemsLink href="#">Item Link</LeftMenuItemsLink>
        </LeftMenuItem>
      </LeftMenuItemsList>
      <PanelRightOrderMax className="panelRightOrderMax">
        {/* Content */}
      </PanelRightOrderMax>
      <MediaQuery932>
        {/* Media Queries */}
      </MediaQuery932>
    </StyledDiv>
  );
};

export default ContentComponent;