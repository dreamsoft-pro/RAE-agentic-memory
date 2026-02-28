import React from 'react';
import {useSelector} from "react-redux";
import Image from "./Image";

const ImagesScrollContainer = (editor, ) => {
    const {columns346, activeIndex} = useSelector(state => state.columnsButtonsReducer);
    const images = useSelector(state => state.imagesReducer.images);
    
    return (
        <div className={"scroll-y-container"}>
            <div
                id="imagesList"
                className={`grid-container ${columns346[activeIndex.images].columns}`}
            >
                {images.map((image, index) => (
                    <Image
                        key={index}
                        editor={editor}
                        {...image}
                    />
                ))}
            </div>
        </div>
    );
}

export default ImagesScrollContainer
