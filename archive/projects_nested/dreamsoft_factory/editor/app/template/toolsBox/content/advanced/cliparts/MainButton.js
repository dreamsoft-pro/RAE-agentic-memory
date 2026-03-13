import React from 'react'

const MainButton = ({usedInModal = false}) => {
    return (
        <button className={`main-tool-button cliparts ${usedInModal ? 'disable-actions' : ""}`}>Cliparty</button>
    )
}

export default MainButton