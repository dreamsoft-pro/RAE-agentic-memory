import React from 'react'
import ToolHelper from "../../toolsBox/navigation/ToolHelper";

const HeaderButton = ({className = "", toolHelperText = "", children, ...props}) => {
    return (
        <button
            className={`navigation-button ${className}`}
            {...props}
        >
            {children}
            <ToolHelper>{toolHelperText}</ToolHelper>
        </button>
    )
}

export default HeaderButton