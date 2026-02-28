import React from 'react'
import {connect} from "react-redux";
import {changeFieldName} from "../../../redux/actions/textToolbar";

function FieldName({fieldName, changeFieldName}){
    return <input className={'inputName'} value={fieldName} onChange={changeFieldName}/>
}
const mapStateToProps = (state) =>{
    return{
        fieldName:state.textToolbar.fieldName
    }
}
const mapDispatchToProps = (dispatch) => {
    return {
        changeFieldName:(name)=>{
            dispatch(changeFieldName(name))
        }
    }
}
export default connect(mapStateToProps, mapDispatchToProps)(FieldName)
