import {getCookie, setCookie} from "../../../helpers/cookies";

export const setColorPickerVisibility = (data) => ({
    type: 'SET_COLOR_PICKER_VISIBILITY',
    payload: data,
})

export const setColorPickerValue = (data) => ({
    type: 'SET_COLOR_PICKER_VALUE',
    payload: data
})

export const setColorPickerOnChangeHandler = (data) => ({
    type: 'SET_COLOR_PICKER_ON_CHANGE_HANDLER',
    payload: data
})

export const setCanCloseColorPickerModal = (data) => ({
    type: 'SET_CAN_CLOSE_COLOR_PICKER_MODAL',
    payload: data
})

export const addNewColorPreset = (data) => ({
    type: 'ADD_NEW_COLOR_PRESET',
    payload: data
});

export const setIsGettingColorFromBitmap = (data) => ({
    type: 'SET_IS_GETTING_COLOR_FROM_BITMAP',
    payload: data
})

const defaultPreviousPresets = [
    'rgba(0, 184, 212, 1)',
    'rgba(255, 99, 132, 0.8)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 0.9)',
    'rgba(255, 159, 64, 1)',
    'rgba(233, 212, 96, 1)',
    'rgba(44, 130, 201, 0.7)',
    'rgba(220, 53, 69, 1)',
    'rgba(40, 167, 69, 1)',
    'rgba(108, 117, 125, 1)'
];

const previousPresets = JSON.parse(getCookie('previousPresets')) || [];

const initialState = {
    colorValue: null,
    isPickerVisible: false,
    canCloseColorPickerModal: false,
    colorPickerOnChangeHandler: () => {},
    isGettingColorFromBitmap: false,
    // those presets below should be replaced with those created in administration mode
    defaultPresets: [
        'rgba(45, 52, 54, 1)',
        'rgba(232, 67, 147, 0.8)',
        'rgba(83, 82, 237, 1)',
        'rgba(255, 234, 167, 1)',
        'rgba(29, 209, 161, 1)',
        'rgba(244, 67, 54, 0.7)',
        'rgba(156, 39, 176, 1)',
        'rgba(3, 169, 244, 1)',
        'rgba(255, 152, 0, 0.9)',
        'rgba(76, 175, 80, 1)',
        'rgba(233, 30, 99, 1)',
        'rgba(121, 85, 72, 1)'
    ],
    previousPresets: [...previousPresets, ...defaultPreviousPresets].slice(0, 12)
};

const colorPickerReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SET_COLOR_PICKER_VISIBILITY':
            return {
                ...state,
                isPickerVisible: action.payload
            };
        case 'SET_COLOR_PICKER_VALUE':
            return {
                ...state,
                colorValue: action.payload
            };
        case 'SET_COLOR_PICKER_ON_CHANGE_HANDLER':
            return {
                ...state,
                colorPickerOnChangeHandler: action.payload
            };
        case 'SET_CAN_CLOSE_COLOR_PICKER_MODAL':
            return {
                ...state,
                canCloseColorPickerModal: action.payload
            };
        case 'ADD_NEW_COLOR_PRESET':
            const {payload: colorValue} = action;

            if (colorValue !== null && !state.previousPresets.includes(colorValue) && !state.defaultPresets.includes(colorValue)) {
                const storedPresets = JSON.parse(getCookie('previousPresets')) || [];
                setCookie('previousPresets', JSON.stringify([colorValue, ...storedPresets.slice(0, 11)]), 7);

                return {
                    ...state,
                    previousPresets: [
                        colorValue,
                        ...state.previousPresets.slice(0, 11)
                    ]
                };
            } else {
                return state;
            }
        case 'SET_IS_GETTING_COLOR_FROM_BITMAP':
            return {
                ...state,
                isGettingColorFromBitmap: action.payload
            }
        default:
            return state;
    }
};

export default colorPickerReducer;
