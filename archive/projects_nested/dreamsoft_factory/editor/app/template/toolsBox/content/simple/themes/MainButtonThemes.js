import React, {Component} from 'react';

export default class MainButtonThemes extends Component {
    constructor(props) {
        super(props);
        this.usedInModal = props.usedInModal || false
    }

    render() {
        return (
            <button
                id="addCreatedTheme"
                className={`main-tool-button themes ${this.usedInModal ? "disable-actions" : ""}`}
            >
                Motywy
            </button>
        );
    }
}