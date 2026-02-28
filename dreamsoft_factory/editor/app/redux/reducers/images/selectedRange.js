const initialState = {
    currentSelectedRange: 'singleElem',
};

const selectedRangeReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SET_CURRENT_SELECTED_RANGE':
            return {
                ...state,
                currentSelectedRange: action.payload,
            };
        default:
            return state;
    }
};

export const setCurrentSelectedRange = (range) => ({
    type: 'SET_CURRENT_SELECTED_RANGE',
    payload: range,
});

export default selectedRangeReducer;
