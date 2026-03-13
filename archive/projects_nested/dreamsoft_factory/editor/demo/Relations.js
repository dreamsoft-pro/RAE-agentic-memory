import React, {Component} from 'react'
import {connect} from 'react-redux'
import ImagesList from "../app/class/tools/ImagesList";

function Ren1(props) {
    return <div>{props.obj.val}</div>
}

function Ren2(props) {
    function handleChange(e) {
        props.obj.val = e.currentTarget.value
        props.onChange(props.obj)
    }

    return <input value={props.obj.val} onChange={handleChange}></input>
}

const theObj = {val: 123}

class Relations extends Component {
    componentDidMount() {
        this.setState({obj: theObj})
    }

    onChange(obj) {
        theObj.val = obj.val
        this.setState({obj: theObj})
    }

    render() {
        return this.state && this.state.obj ? (
            <div><Ren1 obj={this.state.obj}/>
                <Ren2 obj={this.state.obj} onChange={this.onChange.bind(this)}/>
            </div>) : null
    }
}

const mapStateToProps = (state) => {
    return {}
}
const mapDispatchToProps = (dispatch) => {
    return {}
}
export default connect(mapStateToProps, mapDispatchToProps)(Relations)
