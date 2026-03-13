import React from 'react';

const RemoveText = ({ editor, userPage }) => {
  const handleClick = (e) => {
    e.stopPropagation();
    editor.webSocketControllers.userPage.removeProposedText(userPage._id);
  };

  return (
    <div 
      className="editableAreaLeftTool one-less-text notable"
      onClick={handleClick}
    />
  );
};

export default RemoveText;