import React from 'react';
import ToolButton from "./ToolButton";
import ToolHelper from "./ToolHelper";
import {useDispatch, useSelector} from "react-redux";
import {setActiveToolIndex} from "../../../redux/reducers/toolsbox/toolsBox";

const ToolButtonContainer = ({text, index, className = "", ...props}) => {
    const dispatch = useDispatch();
    const activeIndex = useSelector(state => state.toolReducer.activeToolIndex);

    const handleClick = (index) => {
        dispatch(setActiveToolIndex(activeIndex === index ? -1 : index));
    }

    return (
        <div
            {...props}
            className={'tool'}
            onClick={() => handleClick(index)}
        >
            <ToolButton className={className} isActive={activeIndex === index}/>
            <ToolHelper orientation={"x"}>{text}</ToolHelper>
        </div>
    )
}

export default ToolButtonContainer