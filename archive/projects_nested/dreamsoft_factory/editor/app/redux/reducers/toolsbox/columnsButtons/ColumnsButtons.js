export const setToolColumnIndex = (index) => ({
    type: 'SET_TOOL_COLUMN_INDEX',
    payload: index,
});

// reducer.js
const initialState = {
    columns234: [
        {self: "button-2columns", columns: "two-columns"},
        {self: "button-3columns", columns: "three-columns"},
        {self: "button-4columns", columns: "four-columns"}
    ],
    columns346: [
        {self: "button-3columns", columns: "three-columns"},
        {self: "button-4columns", columns: "four-columns"},
        {self: "button-6columns", columns: "six-columns"}
    ],
    activeIndex: {
        images: 0,
        cliparts: 0,
        templates: 0
    }
};

const columnsButtonsReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SET_TOOL_COLUMN_INDEX':
            return {
                ...state,
                activeIndex: {
                    ...state.activeIndex,
                    ...action.payload
                },
            };
        default:
            return state;
    }
};

export default columnsButtonsReducer;
