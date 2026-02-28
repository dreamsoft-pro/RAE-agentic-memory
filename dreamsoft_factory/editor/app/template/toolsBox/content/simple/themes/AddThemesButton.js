import React, {Component} from 'react';

export default class AddThemesButton extends Component {
    constructor(props) {
        super(props);
        this.usedInModal = props.usedInModal || false;
    }

    render() {

        return (
            <span id="addNewTheme" className={`button-themes-second ${this.usedInModal ? "disable-actions" : ""}`}>
                <span id="addNewThemeIcon" className="themeIcon"></span>
                <span id="addNewThemeDesc" className="themeDesc">Zmień strony samemu</span>
            </span>
        );
    }
}