import React from 'react'
import ModalButton from "./ModalButton";

const ModalHeader = ({title, closingButton = true, onCancel = () => {}, children}) => {
    return (
        <div className={"modal-header"}>
            {children}
            <h4 className={"modal-title"}>{title}</h4>
            {closingButton && (
                // propsy
                <ModalButton
                    onClick={() => onCancel()}
                    className={"close-button"}
                />
            )}
        </div>
    )
}

export default ModalHeader