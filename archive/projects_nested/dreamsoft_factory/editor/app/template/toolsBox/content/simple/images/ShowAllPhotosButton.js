import React from "react";

const ShowAllPhotosButton = ({handleClick, usedInModal = false, ...props}) => {
    return (
        <button
            {...props}
            className={`allPhotos default-button ${usedInModal ? "disable-actions" : ""}`}
            onClick={(e) => handleClick(e)}
        />
    )
}

export default ShowAllPhotosButton