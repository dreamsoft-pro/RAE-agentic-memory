import React from "react";

const ShowNotUsedPhotosButton = ({handleClick, usedInModal = false, ...props}) => {
    return (
        <button
            {...props}
            className={`notUsedPhotos default-button ${usedInModal ? "disable-actions" : ""}`}
            onClick={(e) => handleClick(e)}
        />
    )
}

export default ShowNotUsedPhotosButton