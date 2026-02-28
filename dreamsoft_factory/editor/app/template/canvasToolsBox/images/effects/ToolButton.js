import React from 'react'

const ToolButton = ({className = "", isActive, ...props}) => {
    return (
        <button
            className={`${className} ${isActive ? "active" : ""}`}
            {...props}
        />
    )
}

export default ToolButton