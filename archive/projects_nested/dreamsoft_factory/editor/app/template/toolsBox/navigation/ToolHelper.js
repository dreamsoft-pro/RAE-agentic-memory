import React from 'react'

const ToolHelper = ({className = "", orientation = "x", children}) => {
    return (
        <div className={`tool-helper-container ${orientation === "x" ? "x" : "y"} ${className}`}>
            <div className={'tool-helper-content'}>
                <span className={'arrow'}/>
                <span className={'text'}>
                    {children}
                </span>
            </div>
        </div>
    )
}

export default ToolHelper