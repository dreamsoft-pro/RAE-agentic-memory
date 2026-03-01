import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setCurrentSelectedRange } from "../../../../redux/reducers/images/selectedRange";
import ToolButton from './ToolButton';
import { RANGE } from '../../../../Editor';

const RangeOptions = ( { text } ) => {
    const { currentSelectedRange } = useSelector(state => state.range);
    const dispatch = useDispatch();

    useEffect(() => {
        console.log("currrr", currentSelectedRange);
    })

    const handleButtonClick = (range) => {
        dispatch(setCurrentSelectedRange(range));
    };

    const renderText = () => {
        switch (currentSelectedRange) {
            case RANGE.singleElem:
                return "Zastosuj tylko dla bieżącego zdjęcia.";
            case RANGE.allElemInPage:
                return "Zastosuj dla zdjęć na tej stronie.";
            case RANGE.allElemInProject:
                return "Zastosuj dla wszystkich zdjęć w projekcie.";
            default:
                return "Zastosuj dla zdjęcia.";
        }
    };

    return (
        <div className='apply-options-container'>
            <div className='content-header'>
                <p>{text}</p>
                <div className='photo-options-container tools-buttons-container'>
                    <ToolButton 
                        key='current-photo'
                        className='button-option current-photo selected-item-tool-button'
                        isActive={currentSelectedRange === RANGE.singleElem}
                        onClick={() => handleButtonClick(RANGE.singleElem)}
                    />
                    <ToolButton 
                        key='all-photos-page'
                        className='button-option all-photos-page selected-item-tool-button'
                        isActive={currentSelectedRange === RANGE.allElemInPage}
                        onClick={() => handleButtonClick(RANGE.allElemInPage)}
                    />
                    <ToolButton 
                        key='all-photos-project'
                        className='button-option all-photos-project selected-item-tool-button'
                        isActive={currentSelectedRange === RANGE.allElemInProject}
                        onClick={() => handleButtonClick(RANGE.allElemInProject)}
                    />
                </div>
                <p>{renderText()}</p>
            </div>
        </div>
    );
};

export default RangeOptions;
