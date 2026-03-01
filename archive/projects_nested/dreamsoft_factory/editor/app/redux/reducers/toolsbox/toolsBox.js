export const setActiveToolIndex = (index) => ({
    type: 'SET_ACTIVE_TOOL_INDEX',
    payload: index,
});

// reducer.js
const initialState = {
    activeToolIndex: 0,
};

const toolReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SET_ACTIVE_TOOL_INDEX':
            return {
                ...state,
                activeToolIndex: action.payload,
            };
        default:
            return state;
    }
};

export default toolReducer;
