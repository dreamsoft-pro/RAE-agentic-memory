import React, {Component} from 'react';

export default class CopyFromThemeButton extends Component {
    constructor(props) {
        super(props);
        this.usedInModal = props.usedInModal || false
    }

    render() {

        return (
            <span id="copyThemesFrom" className={`button-themes-second ${this.usedInModal ? "disable-actions" : ""}`}>
                <span id="copyThemesFromIcon" className="themeIcon"></span>
                <span id="copyThemesFromDesc" className="themeDesc">Zmień wszystkie motywy</span>
            </span>
        );
    }
}