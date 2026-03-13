import React from 'react';
import { useSelector } from 'react-redux';
import { ButtonList } from './ButtonList';
import ToolButton from './ToolButton';

const CanvasToolBar = ({ editor, userPage }) => {
  const editorType = useSelector((state) => state.projectReducer.editorType);

  return (
    <>
      {ButtonList.map(({ id, Component, helperText, showAlways }) => (
        (showAlways || editorType === 'user') && (
          <ToolButton
            key={id}
            Component={Component}
            helperText={helperText}
            editor={editor}
            userPage={userPage}
          />
        )
      ))}
    </>
  );
};

export default CanvasToolBar;