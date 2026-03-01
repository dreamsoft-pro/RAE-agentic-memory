import React from 'react';
import ThemesScrollList from './ThemesScrollList';
import AddCopyButtonContainer from './AddCopyButtonContainer';
import ThemesButtonsList from "../../../buttons/ThemesButtonsList";

const ThemesToolContent = ({editor, className = ""}) => {
    return (
        <div id={"themesContent"} className={`themes-inner-container ${className}`}>
            <div className={'buttons-wrapper'}>
                <div className={'buttons-container'}>
                    <ThemesButtonsList.Components.MainButton.Component/>
                </div>
                <div className={'buttons-container'}>
                    <AddCopyButtonContainer/>
                </div>
            </div>
            <ThemesScrollList editor={editor} />
        </div>
    )
}

export default ThemesToolContent;
