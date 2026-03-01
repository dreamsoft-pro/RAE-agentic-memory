export const setEditorType = (data) => ({
    type: 'UPDATE_EDITOR_TYPE',
    payload: data,
});

export const setProjectThemes = (data) => ({
    type: 'SET_PROJECT_THEMES',
    payload: data,
})

export const changeEditingText = (data) => ({
    type: "CHANGE_EDITING_TEXT",
    payload: data,
});


export const setEditingTextEffects = () => ({
    type: "SET_EDITING_TEXT_EFFECTS",
})

export const changeFullScreenMode = (data) => ({
    type: "CHANGE_FULL_SCREEN_MODE",
    payload: data
})

const initialState = {
    themes: [],
    // user / advancedUser / admin / advancedAdmin
    editorType: "user",
    fullScreenMode: false,
    text: {
        active: false,
        effects: false,
    }
};

const projectReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'CHANGE_EDITING_TEXT':
            return {
                ...state,
                text: {
                    ...state.text,
                    active: action.payload
                }
            };
        case 'CHANGE_FULL_SCREEN_MODE':
            return {
                ...state,
                fullScreenMode: action.payload
            }
        case 'UPDATE_EDITOR_TYPE':
            return {
                ...state,
                editorType: action.payload,
            };
        case 'SET_PROJECT_THEMES':
            return {
                ...state,
                themes: action.payload
            };
        case 'SET_EDITING_TEXT':
            return {
                ...state,
                text: !state.text.active
            };

        case 'SET_EDITING_TEXT_EFFECTS':
            return {
                ...state,
                text: {
                    ...state.text,
                    effects: !state.text.effects
                }
            };
        default:
            return state;
    }
};

export default projectReducer;
