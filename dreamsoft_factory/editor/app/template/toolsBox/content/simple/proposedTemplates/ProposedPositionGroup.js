import React, {useEffect, useState} from 'react';
import {useSelector} from "react-redux";
import {store} from "../../../../../ReactSetup";
import {setExpandedSelectors} from "../../../../../redux/reducers/templates/templates";

const ProposedPositionGroup = ({group, usedInModal, index, editor}) => {
    const {columns234, activeIndex} = useSelector(state => state.columnsButtonsReducer);
    const {expandedSelectors} = useSelector(state => state.templatesReducer);

    // current editing page (canva)
    const currentPage = editor.userProject.getCurrentView().Pages[0]

    const [previousTemplateId, setPreviousTemplateId] = useState(currentPage.ProposedTemplateFrom)


    const handleMouseEnter = (template) => {
        editor.webSocketControllers.userPage.setProposedTemplate(currentPage._id, template._id);
    }

    const handleMouseLeave= () => {
        editor.webSocketControllers.userPage.setProposedTemplate(currentPage._id, previousTemplateId);
    }

    const handleClick = (template) => {
        // local proposedTemplates won't set
        setPreviousTemplateId(template._id)
        editor.webSocketControllers.userPage.setProposedTemplate(currentPage._id, template._id);
    }

    const {imagesCount, open} = expandedSelectors[index];

    return (
        <div className={"layout-group-container"}>
            <ProposedTemplateGroupButton
                isActive={open}
                group={group}
                usedInModal={usedInModal}
                index={index}
                imagesCount={imagesCount}
            />
            <div
                className={`grid-container ${columns234[activeIndex.templates].columns} ${open ? "" : "hidden"}`}
            >
                {group.map((template, index) => (
                    <div
                        onMouseEnter={() => handleMouseEnter(template)}
                        onMouseLeave={() => handleMouseLeave()}
                        onClick={() => handleClick(template)}
                        key={index}
                        className={`layout proposedTemplateElement ${currentPage?.ProposedTemplateFrom === template._id ? "active" : ""}`}
                        style={{
                            backgroundImage: `url(${EDITOR_ENV.staticUrl + template.url})`,
                        }}
                        data-id={template._id}
                    />
                ))}
            </div>
        </div>
    )
}

export default ProposedPositionGroup

const ProposedTemplateGroupButton = ({group, imagesCount, isActive, usedInModal, index}) => {

    const {expandedSelectors} = useSelector(state => state.templatesReducer)
    // proper word format, depending on the number of photos count (liczebniki)
    const getPhotoLabel = (number) => {
        const lastDigit = number % 10;
        const lastTwoDigits = number % 100;

        if (lastTwoDigits >= 12 && lastTwoDigits <= 14) {
            return `${imagesCount} Zdjęć`; // Specjalne przypadki 12, 13, 14
        }

        if (lastDigit === 1) {
            return `${imagesCount} Zdjęcie`;
        } else if (lastDigit >= 2 && lastDigit <= 4) {
            return `${imagesCount} Zdjęcia`;
        } else {
            return `${imagesCount} Zdjęć`;
        }
    }

    const handleClick = (groupIndex) => {
        store.dispatch(setExpandedSelectors(expandedSelectors.toSpliced(groupIndex, 1, {
            ...expandedSelectors[groupIndex],
            open: !expandedSelectors[groupIndex].open
        })))
    }

    return (
        <div
            className={`list-button ${isActive ? "active" : ""} ${usedInModal ? "disable-actions" : ""}`}
            onClick={() => handleClick(index)}
        >
            <span>{getPhotoLabel(imagesCount)}</span>
            <span className="layout-group-count">{group.length}</span>
        </div>
    )
}