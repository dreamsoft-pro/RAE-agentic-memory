import React, {Component} from 'react';
import CopyFromThemeButton from './CopyFromThemeButton';
import AddThemesButton from './AddThemesButton';
import ThemesButtonsList from "../../../buttons/ThemesButtonsList";

export default class AddCopyButtonContainer extends Component {
    constructor(props) {
        super(props);
    }

    render() {

        return (
            <>
                <ThemesButtonsList.Components.AddThemes.Component/>
                <ThemesButtonsList.Components.CopyFromTheme.Component/>
            </>
        );
    }
}