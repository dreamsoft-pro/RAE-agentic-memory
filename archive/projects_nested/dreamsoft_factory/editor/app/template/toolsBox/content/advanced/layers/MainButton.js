import React from 'react'

const MainButton = ({usedInModal = false}) => {
    return (
        <div className={`main-tool-button layers ${usedInModal ? 'disable-actions' : ""}`}>Warstwy</div>
    )
}

export default MainButton