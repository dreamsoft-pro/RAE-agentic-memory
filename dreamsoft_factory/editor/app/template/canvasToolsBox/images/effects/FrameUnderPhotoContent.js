import React, { useEffect, useState } from "react";
import RangeOptions from "./RangeOptions";
import Switch from "../../../../components/Switch";
import { useSelector } from "react-redux";

const FrameUnderPhotoContent = () => {
    const [framesList, setFramesList] = useState([]);
    const [selectedFrameId, setSelectedFrameId] = useState(null);

    const { proposedPositionInstance } = useSelector(state => state.selectedImageReducer);
    const { currentSelectedRange } = useSelector(state => state.range);
    const editorType = useSelector(state => state.projectReducer.editorType);

    const backgroundFrame = useSelector(state => state.proposedPositionBridge.backgroundFrame);

    useEffect(() => {
        if (proposedPositionInstance) {

            handleFrameChange(true);

            // To dziala na dev!?
            // const userThemePage = editorType === 'user' 
            //     ? proposedPositionInstance.editor.userPage.ThemePageFrom 
            //     : proposedPositionInstance.editor.userPage.ThemePageFrom;

            //Tu obiekt nie dziala a powinno z racji uzywania w poprzednim toolsboxie oraz wersji produkcyjnej!!!!!
            const userThemePage = editorType === 'user' 
                ? proposedPositionInstance.parentPage.userPage.ThemePageFrom 
                : proposedPositionInstance.getFirstImportantParent().userPage.ThemePageFrom;


            proposedPositionInstance.editor.webSocketControllers.themePage.getThemeBackgroundFrames(userThemePage, data => {
                setFramesList(data.backgroundFrames.map(f => ({
                    _id: f._id,
                    thumbnail: EDITOR_ENV.staticUrl + f.ProjectImage.thumbnail,
                    helper: { x: f.x, y: f.y, width: f.width, height: f.height }
                })));
            });
        }
    }, [proposedPositionInstance]);

    const handleFrameChange = (checked) => {
        proposedPositionInstance.editor.getEditableObjectsByType(currentSelectedRange, 'ProposedPosition')
            .forEach(p => {
                p.backgroundFrame = checked;
                if (checked) {
                    p.backgroundFrameID=selectedFrameId
                    proposedPositionInstance.editor.webSocketControllers.frameObject.get(selectedFrameId, data => {
                        p.setBackgroundFrame(data);

                    });
                } else {
                    p.removeBackgroundFrame()
                }

                proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                    p.dbID,
                    {
                        backgroundFrame: checked,
                        backgroundFrameID: selectedFrameId
                    }
                );
            })
    };

    const handleFrameSelect = (frameId) => {
        setSelectedFrameId(frameId);
        handleFrameChange(backgroundFrame);
    };

    return (
        <>
            <RangeOptions text='Opcje ramki za zdjęciem:' />
            <div className='switch-container'>
                <Switch
                    label={{
                        close: "Wyłącz ramkę",
                        open: "Włącz ramkę"
                    }}
                    onChange={() => handleFrameChange(!backgroundFrame)}
                    checked={backgroundFrame}
                />
            </div>
            <div className={'scroll-y-container'}>
                <div className={'grid-container three-columns padding'}>
                    {framesList.map(frame => (
                        <div 
                            key={frame._id}
                            data-id={frame._id}
                            className={'photo-item'}
                            onClick={() => handleFrameSelect(frame._id)}
                        >
                            <img src={frame.thumbnail} alt="Frame thumbnail" />
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
};

export default FrameUnderPhotoContent;
