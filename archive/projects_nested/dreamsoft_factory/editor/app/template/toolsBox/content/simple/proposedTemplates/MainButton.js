import React, {Component} from 'react';

export default class MainButton extends Component {
    constructor(props) {
        super(props);
        this.usedInModal = props.usedInModal || false;
    }

    render() {
        return (
            <button className={`main-tool-button templates ${this.usedInModal ? "disable-actions" : ""}`}>
                Układ zdjęć
            </button>
        );
    }
}