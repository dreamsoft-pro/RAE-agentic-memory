import React from 'react';
import ToolHelperCanvas from './ToolHelperCanvas';
const ToolButton = ({ Component, helperText, editor, userPage }) => {

    return (
      <div className="canvas-tool-wrapper" >
        <Component editor={editor} userPage={userPage} />
        <ToolHelperCanvas text={helperText} />
      </div>    
    );
  };

  export default ToolButton;