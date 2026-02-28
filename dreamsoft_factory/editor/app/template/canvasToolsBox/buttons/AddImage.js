import React from 'react';
import { useSelector } from 'react-redux';

const AddImage = ({ editor, userPage, userType }) => {

  const editorType = useSelector((state) => state.projectReducer.editorType);

  const handleClick = (e) => {
    e.stopPropagation();

    if (editorType === 'user') {
      editor.webSocketControllers.userPage.oneMoreImage(
        userPage._id,
        userPage.ProposedTemplate._id
      );
    } else if (editorType === 'advancedUser') {
      const width = editor.trueWidth < 200 ? (editor.trueWidth - 20) : 200;
      const height = editor.trueHeight < 200 ? (editor.trueHeight - 20) : 200;
      const x = editor.trueWidth / 2;
      const y = editor.trueHeight / 2;

      editor.webSocketControllers.userPage.addEmptyProposedPosition(
        userPage._id, 
        userPage.ProposedTemplate._id,
        width,
        height,
        x,
        y
      );
    }
  };

  return (
    <div 
      className="editableAreaLeftTool one-more-image notable"
      onClick={handleClick}
    />
  );
};

export default AddImage;