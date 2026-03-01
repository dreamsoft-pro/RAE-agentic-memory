import React, { Component } from 'react';

export default class VisibilityToggle extends Component {
    constructor(props) {
        super(props);
        this.usedInModal = props.usedInModal || false;
    }

    render() {
        return (
            <span className={`objectVisibilityModal visible ${this.usedInModal ? "disable-actions" : ""}`} />
        );
    }
}
