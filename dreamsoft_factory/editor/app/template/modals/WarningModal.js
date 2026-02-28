import React from 'react';
import ModalButton from "./components/ModalButton";
import ModalFooter from "./components/ModalFooter";
import ModalBody from "./components/ModalBody";
import ModalHeader from "./components/ModalHeader";
import ModalContent from "./components/ModalContent";

const WarningModal = ({id, content, confirm, abort, confirmText = "Rozumiem"}) => {
    return (
        <ModalContent id={id}>
            <ModalHeader
                title={"Uwaga"}
                onCancel={abort}
            />
            <ModalBody>
                <div className='warning-icon'>
                </div>
                <div className="warning-info warning-description">
                    {content}
                </div>
            </ModalBody>
            <ModalFooter>
                <ModalButton
                    className={"btn cancel-button"}
                    onClick={abort ? () => abort() : () => {}}
                    text={"Anuluj"}
                />
                <ModalButton
                    className={"btn danger-button"}
                    onClick={() => confirm()}
                    text={confirmText}
                />
            </ModalFooter>
        </ModalContent>
    )
}

export default WarningModal