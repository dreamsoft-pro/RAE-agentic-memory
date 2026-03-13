export const setProjectImages = (data) => ({
    type: 'SET_PROJECT_IMAGES',
    payload: data,
});

export const addProjectImage = (data) => ({
    type: 'ADD_PROJECT_IMAGE',
    payload: data,
})

export const setPhotoRemovingData = (data) => ({
    type: "SET_PHOTO_REMOVING_DATA",
    payload: data
})

export const removeUserImage = (data) => ({
    type: "REMOVE_USER_IMAGE",
    payload: data
})

export const setProjectImageCounter = (data) => ({
    type: "SET_PROJECT_IMAGE_COUNTER",
    payload: data
})

const initialState = {
    images: [],
    removingImageData: {},
};

const imagesReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SET_PROJECT_IMAGES':
            return {
                ...state,
                images: action.payload,
            };
        case "SET_PHOTO_REMOVING_DATA":
            return {
                ...state,
                removingImageData: action.payload
            };
        case "ADD_PROJECT_IMAGE":
            return {
                ...state,
                images: [...state.images, action.payload]
            };
        case "REMOVE_USER_IMAGE":
            return {
                ...state,
                images: state.images.filter(image => image.uid !== action.payload.imageUID)
            };
        case "SET_PROJECT_IMAGE_COUNTER":
            return {
                ...state,
                images: state.images.map(image => (
                    image.uid === action.payload.uid ? {
                        ...image,
                        useCount: action.payload.count,
                        used: action.payload.count > 0
                    } :
                    image
                ))
            };
        default:
            return state;
    }
};

export default imagesReducer;
