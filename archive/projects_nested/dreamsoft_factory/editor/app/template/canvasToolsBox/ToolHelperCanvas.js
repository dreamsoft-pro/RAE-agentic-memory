import React from 'react';

const ToolHelperCanvas = ({ text }) => {
    return (
        <div className="tool-helper-container x">
            <div className="tool-helper-content">
                <span className="arrow"></span>
                <span className="text">{text}</span>
            </div>
        </div>
    );
};

export default ToolHelperCanvas;