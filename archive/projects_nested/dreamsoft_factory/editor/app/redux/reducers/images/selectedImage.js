export const setProposedPositionInstance = (data) => ({
    type: "SET_PROPOSED_POSITION_INSTANCE",
    payload: data
})

export const setCurrentSelectedImageToolIndex = (data) => ({
    type: "SET_CURRENT_SELECTED_IMAGE_TOOL_INDEX",
    payload: data
})

export const setEditingImageEffects = () => ({
    type: "SET_EDITING_IMAGE_EFFECTS",
})

export const setEditingImagePosition = () => ({
    type: "SET_EDITING_IMAGE_POSITION",
})

export const changeEditingImage = (data) => ({
    type: "CHANGE_EDITING_IMAGE",
    payload: data,
});

const initialState = {
    proposedPositionInstance: null,
    currentToolIndex: 0,
    properties: {
        opacity: 1
    },
    selectedImage: {
        active: false,
        effects: false,
        position: false,
    },
};

const selectedImageReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'CHANGE_EDITING_IMAGE':
            return {
                ...state,
                selectedImage: {
                    active: action.payload,
                    effects: !action.payload ? false : state.selectedImage.effects,
                    position: !action.payload ? false : state.selectedImage.position,
                }
            };
        case "SET_PROPOSED_POSITION_INSTANCE":
            return {
                ...state,
                proposedPositionInstance: action.payload
            }
        case "SET_CURRENT_SELECTED_IMAGE_TOOL_INDEX":
            return {
                ...state,
                currentToolIndex: action.payload
            }

        case 'SET_EDITING_IMAGE_EFFECTS':
            return {
                ...state,
                selectedImage: {
                    ...state.selectedImage,
                    position: false,
                    effects: !state.selectedImage.effects
                }

            };
        case 'SET_EDITING_IMAGE_POSITION':
            return {
                ...state,
                selectedImage: {
                    ...state.selectedImage,
                    effects: false,
                    position: !state.selectedImage.position
                }
            };
        default:
            return state;
    }
};

export default selectedImageReducer;
