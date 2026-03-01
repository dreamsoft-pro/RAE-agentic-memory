import React from 'react';
import { useSelector } from 'react-redux';

const AddText = ({ editor, userPage}) => {


  const editorType = useSelector((state) => state.projectReducer.editorType);

  const handleClick = (e) => {
    e.stopPropagation();
    
    if (editorType === 'user') {
      editor.webSocketControllers.userPage.oneMoreText(
        userPage._id,
        userPage.ProposedTemplate._id
      );
    } else if (editorType === 'advancedUser') {
      const textSize = {
        height: 23,
        width: editor.trueWidth < 200 ? editor.trueWidth / 2 : 200
      };

      editor.webSocketControllers.userPage.addProposedText(
        userPage._id,
        textSize.width,
        textSize.height,
        editor.trueWidth / 2,
        editor.trueHeight / 2
      );
    }
  };

  return (
    <div 
      className="editableAreaLeftTool one-more-text notable"
      onClick={handleClick}
    />
  );
};

export default AddText;