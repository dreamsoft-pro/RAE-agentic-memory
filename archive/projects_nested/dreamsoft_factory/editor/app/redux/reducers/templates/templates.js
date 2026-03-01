export const updateTemplatesData = (data) => ({
    type: 'UPDATE_TEMPLATES_DATA',
    payload: data,
});

export const updateTemplatesShowingType = () => ({
    type: "UPDATE_TEMPLATES_SHOWING_TYPE",
});

export const setExpandedSelectors = (data) => ({
    type: "SET_EXPANDED_SELECTORS",
    payload: data
})

const initialState = {
    data: [],
    allTemplates: true,
    expandedSelectors: [],
};

const templatesReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'UPDATE_TEMPLATES_DATA':
            return {
                ...state,
                data: action.payload,
            };
        case 'UPDATE_TEMPLATES_SHOWING_TYPE':
            return {
                ...state,
                allTemplates: !state.allTemplates
            };
        case 'SET_EXPANDED_SELECTORS':
            return {
                ...state,
                expandedSelectors: action.payload
            };
        default:
            return state;
    }
};

export default templatesReducer;
