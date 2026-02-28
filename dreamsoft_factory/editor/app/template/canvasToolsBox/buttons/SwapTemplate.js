import React, { useEffect, useRef } from 'react';

const SwapTemplate = ({ editor, userPage }) => {

  const handleClick = (e) => {
    e.stopPropagation();
    editor.webSocketControllers.userPage.swapTemplate(
      userPage._id, 
      userPage.ProposedTemplate._id
    );
  };

  return (
    <div 
      className="editableAreaLeftTool swap-template"
      onClick={handleClick}
    >
    </div>
  );
};

export default SwapTemplate;