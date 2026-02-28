/**
 * Generates a button to toggle all layouts with a dropdown icon
 */
import React from 'react'

const AllLayoutsButton = ({toggleAllLayouts, isActive = false, usedInModal = false}) => {
    return (
        <div
            className={`list-button ${isActive ? "active" : ""} ${usedInModal ? "disable-actions" : ""}`}
            onClick={() => !usedInModal ? toggleAllLayouts() : {}}
        >
            Wszystkie układy
        </div>
    )
}

export default AllLayoutsButton
