import React from 'react'

const CategorySelector = ({usedInModal = false}) => {
    const clipartsOptions = [
        {name: "KATEGORIA"},
        {name: "Myszka Miki"},
    ];

    return (
        <div className={`select-container ${usedInModal ? "disable-actions" : ""}`}>
            <select name={"cliparts"} defaultValue={clipartsOptions[0].name}>
                {clipartsOptions.map((option, index) => (
                    <option key={index} value={option.name}>{option.name}</option>
                ))}
            </select>
        </div>
    )
}

export default CategorySelector