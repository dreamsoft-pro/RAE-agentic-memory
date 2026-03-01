import {Provider} from 'react-redux';
import React, {Component} from 'react';
import ReactSetup from '../app/ReactSetup'
import List from "./List";
import Easel from "./Easel";
import ListEffects from "./ListEffects";
import Shadowed from './Shadowed'
import Relations from './Relations'
import Tweens from './Tweens'
import TextTools from "./TextTools";

export class Demo extends Component {

    state = {startComponent: null}

    componentDidMount() {
        const compName = window.location.hash ? window.location.hash.substring(1) : 'DefaultApp'
        let startComponent
        switch (compName) {
            case 'Relations':
                startComponent = Relations
                break;
            case 'TextTools':
                startComponent = TextTools
                break;
            case 'Shadowed':
                startComponent = Shadowed
                break;
            case 'List':
                startComponent = List
                break;
            default :
                startComponent = Tweens
                break;
        }
        this.setState({startComponent})

        /*import(`${appFile}`)
            .then((module) => {
                this.setState({startComponent: module.default})
            }).catch((e) => {
            console.error(e)
        })*/

    }

    render() {
        const ToRender = this.state.startComponent;
        return ToRender ? <React.Fragment>
                <ToRender/>
            </React.Fragment>
            : null;
    }
}

