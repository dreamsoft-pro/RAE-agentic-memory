import React from 'react';

const ToolButton = ({isActive, usedInModal = false, className = ""}) => {
    return (
        <button
            className={`tool-button tool-helper-button ${className} ${usedInModal ? "disable-actions active" : ""} ${isActive ? "active" : ""}`}
        >
        </button>
    )
}

export default ToolButton;