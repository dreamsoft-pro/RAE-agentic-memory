import React, { Component } from 'react';

export default class Brush extends Component {
    constructor(props) {
        super(props);
        this.usedInModal = props.usedInModal || false;
    }

    render() {
        return (
            <span className={`objectBrushModal ${this.usedInModal ? "disable-actions" : ""}`} />
        );
    }
}
