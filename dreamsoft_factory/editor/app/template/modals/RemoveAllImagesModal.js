import React from 'react'
import WarningModal from "./WarningModal";

const RemoveAllImagesModal = ({editor}) => {
    const handleConfirm = () => {
        editor.webSocketControllers.userProject.removeAllImages(
            editor.userProject.getID()
        );
    }

    return (
        <WarningModal
            id={"removeAllImagesModal"}
            content={"Usunięcie zdjęć spowoduje wyczyszczenie projektu!"}
            confirm={handleConfirm}
        />
    )
}

export default RemoveAllImagesModal