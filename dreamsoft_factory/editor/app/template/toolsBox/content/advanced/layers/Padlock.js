import React, { Component } from 'react';

export default class Padlock extends Component {
    constructor(props) {
        super(props);
        this.usedInModal = props.usedInModal || false;
    }

    render() {
        return (
            <span className={`objectPadlockModal ${this.usedInModal ? "disable-actions" : ""}`} />
        );
    }
}
