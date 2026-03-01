import React from 'react'

const MainButton = ({usedInModal = false}) => {
    return (
        <div className={`main-tool-button positions ${usedInModal ? 'disable-actions' : ""}`}>Wymiary i Pozycja</div>
    )
}

export default MainButton