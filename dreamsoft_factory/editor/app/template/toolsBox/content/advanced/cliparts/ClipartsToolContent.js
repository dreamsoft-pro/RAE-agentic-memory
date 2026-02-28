import React from 'react';
import ClipartsButtonsList from '../../../buttons/ClipartsButtonsList';
import {useSelector} from "react-redux";

const ClipartsToolContent = ({editor, className = ""}) => {
    const {columns234, activeIndex} = useSelector(state => state.columnsButtonsReducer)
    // Handle click events for proposed proposedTemplates
    const handleProposedTemplateClick = (e) => {
        e.stopPropagation();

        if (e.target.classList.contains('proposedTemplateElement')) {
            editor.webSocketControllers.userPage.setProposedTemplate(
                editor.userProject.getCurrentView().Pages[0]._id,
                e.target.getAttribute('id')
            );
        }
    };

    return (
        <div id="cliparts-content" className={`inner-container ${className}`}>
            <div className="buttons-wrapper">
                <div className={'buttons-container'}>
                    <ClipartsButtonsList.Components.MainButton.Component/>
                    <ClipartsButtonsList.Components.ChangeColumns.Component/>
                </div>
                <div className={'buttons-container'}>
                    <ClipartsButtonsList.Components.CategorySelector.Component/>
                </div>
            </div>
            <div
                id={"clipartsList"}
                className={`grid-container ${columns234[activeIndex.cliparts].columns}`}
                onClick={(e) => handleProposedTemplateClick(e)}
            ></div>
        </div>
    );
};

export default ClipartsToolContent;
