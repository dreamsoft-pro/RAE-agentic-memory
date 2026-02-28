import React, { useEffect, useRef } from "react";
import {EditableArea} from "../../../../../class/editablePlane";
import {store} from "../../../../../ReactSetup";
import {setPhotoRemovingData} from "../../../../../redux/reducers/images/images";

const PhotoItem = ({ editor, ...props }) => {
    const objectRef = useRef(null);
    const statusBarRef = useRef(null);

    useEffect(() => {
        const object = objectRef.current;

        if (object) {
            // Make the object draggable using jQuery
            $(object).draggable({
                appendTo: "body",
                zIndex: 1000000,
                cursorAt: { left: -20, top: -20 },
                start: () => {
                    editor.stage.preparePagesToDrop();
                },
                drag: (event) => {
                    const areas = editor.stage.getEditableAreas();

                    for (const key in areas) {
                        if (areas[key]) {
                            const local = areas[key].globalToLocal(event.clientX, event.clientY - 80);
                            const bounds = areas[key].getBounds();
                            // You can process local and bounds as needed
                        }
                    }
                },
                stop: (event) => {
                    event.bubbles = false;
                    event.stopPropagation();
                    const overObjects = [];

                    editor.getStage()._getObjectsUnderPoint(event.clientX, event.clientY - 75, overObjects);


                    for (var i = 0; i < overObjects.length; i++) {
                        if (overObjects[i].target) {
                            if (overObjects[i].target instanceof EditableArea)
                                console.log("propsy", props)
                                event.bitmapObject = props; // Attach image info
                                overObjects[i].dispatchEvent(event);
                                editor.stage.stopPageDroping();
                        }
                    }

                    editor.stage.stopPageDroping();
                },
                revert: false,
                helper: "clone",
            });
        }
    }, []);

    const handleClick = () => {
        store.dispatch(setPhotoRemovingData({
            projectId: editor.userProject.getID(),
            uid: props.uid
        }))
    }

    const uploadStatusClass = props.thumbnail && props.minUrl && props.imageUrl ? "uploaded" : "";

    return (
        <div
            ref={objectRef}
            className={`photo-item ${uploadStatusClass} ${props.used ? "used" : ""}`}
            data-uid={props.uid}
            style={{backgroundImage: `url(${props.thumbnail})`}}
        >
            <span className={uploadStatusClass}></span>
            {!props.uploaded ? (
                <div ref={statusBarRef} className="statusBar">
                    <div className="statusProgress"></div>
                </div>
            ) : (
                <span className="usedCounter">{props.useCount}</span>
            )}
            <button
                data-bs-toggle={"modal"}
                data-bs-target={"#removeSinglePhotoModal"}
                className={"remover"}
                data-id={props.dbID}
                onClick={() => handleClick()}
            />
        </div>
    );
};

export default PhotoItem;
