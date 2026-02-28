import React from 'react';

const RemoveImage = ({ editor, userPage }) => {
  const handleClick = (e) => {
    e.stopPropagation();
    editor.webSocketControllers.userPage.removeOneProposedImage(userPage._id);
  };

  return (
    <div 
      className="editableAreaLeftTool one-less-image notable"
      onClick={handleClick}
    />
  );
};

export default RemoveImage;