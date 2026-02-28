import React from 'react'
import WarningModal from "./WarningModal";
import {useSelector} from "react-redux";
import {setPhotoRemovingData} from "../../redux/reducers/images/images";
import {store} from "../../ReactSetup";

const RemoveSinglePhotoModal = ({editor}) => {
    const { removingImageData } = useSelector(state => state.imagesReducer);

    const handleConfirm = () => {
        const { projectId, uid } = removingImageData

        editor.webSocketControllers.userProject.removePhoto(projectId, uid);

        // after deleting the image, set blank object
        store.dispatch(setPhotoRemovingData({}))
    }

    return (
        <WarningModal
            id={"removeSinglePhotoModal"}
            content={'Usunięcie zdjęcia spowoduje usunięcie pliku, oraz wszystkich jego wystąpień w projekcie.'}
            confirm={handleConfirm}
        />
    )
}

export default RemoveSinglePhotoModal