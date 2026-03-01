import React from 'react';

const ToolOptionButton = ({ isActive, text, ...props }) => {
    return (
        <button
            {...props}
            className={`navigation-button-switcher ${isActive ? 'active' : ''}`}
        >
            {text}
        </button>
    );
};

export default ToolOptionButton;
