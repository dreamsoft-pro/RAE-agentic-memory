import {combineReducers} from 'redux';
import {textToolbar} from "./textToolbar";
import {text2Bridge} from './text2Bridge'
import {proposedPositionToolbarReducer} from './proposedPositionToolbarReducer'
import {proposedPositionBridgeReducer} from './proposedPositionBridgeReducer'
import toolReducer from "./toolsbox/toolsBox";
import templatesReducer from "./templates/templates";
import columnsButtonsReducer from "./toolsbox/columnsButtons/ColumnsButtons";
import projectReducer from "./project/project";
import imagesReducer from "./images/images";
import angleReducer from './toolsbox/angleReducer';
import { carouselReducer } from './carousel/carousel';
import selectedImageReducer from "./images/selectedImage";
import selectedRangeReducer from './images/selectedRange';
import colorPickerReducer from "./colorPicker/colorPickerReducer";

export default combineReducers({
    textToolbar,
    text2Bridge,
    proposedPositionToolbar: proposedPositionToolbarReducer,
    proposedPositionBridge: proposedPositionBridgeReducer,
    toolReducer,
    templatesReducer,
    columnsButtonsReducer,
    projectReducer,
    imagesReducer,
    angleReducer,
    carouselReducer,
    selectedImageReducer,
    range: selectedRangeReducer,
    colorPickerReducer
})

