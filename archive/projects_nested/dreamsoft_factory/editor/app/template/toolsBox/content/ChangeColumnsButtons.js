import React from 'react';
import {useSelector} from "react-redux";
import {store} from "../../../ReactSetup";
import {setToolColumnIndex} from "../../../redux/reducers/toolsbox/columnsButtons/ColumnsButtons";

const ChangeColumnsButtons = ({usedInModal = false, option = "images"}) => {
    const {activeIndex, columns234, columns346} = useSelector(state => state.columnsButtonsReducer);

    const buttons = ["templates", "cliparts"].some(value => value === option) ? columns234 : columns346;

    const handleColumnChange = (index) => {
        console.log("data", {[option]: index})
        store.dispatch(setToolColumnIndex({[option]: index}));
    };

    return (
        <div className={`columns-type-container ${usedInModal ? "disable-actions" : ""}`}>
            {buttons.map((button, index) => (
                <button
                    key={index}
                    className={`${index === activeIndex[option] ? "active" : ""} ${button.self}`}
                    onClick={() => handleColumnChange(index)}
                ></button>
            ))}
        </div>
    );
};

export default ChangeColumnsButtons;