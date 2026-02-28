import React from 'react'

const ModalContent = ({className = "", children, ...props}) => {
    return (
        <div
            className={`modal fade ${className}`}
            tabIndex={"-1"}
            role={"dialog"}
            aria-hidden={"true"}
            {...props}
        >
            <div className={"modal-dialog"} role={"document"}>
                <div className={"modal-content"}>
                    {children}
                </div>
            </div>
        </div>
    )
}

export default ModalContent