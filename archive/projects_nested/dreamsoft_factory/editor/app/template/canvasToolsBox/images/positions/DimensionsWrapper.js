import React, {useState, useEffect} from 'react';
import { ConnectButton } from './buttons/ConnectButton';
import { useSelector } from 'react-redux';

const DimensionsWrapper = () => {
    const { proposedPositionInstance } = useSelector(state => state.selectedImageReducer);

    const [width, setWidth] = useState(proposedPositionInstance.width);
    const [height, setHeight] = useState(proposedPositionInstance.height);
    const [x, setX] = useState(proposedPositionInstance.x);
    const [y, setY] = useState(proposedPositionInstance.y);
    const [isConnected, setIsConnected] = useState(false);
    const [aspectRatio, setAspectRatio] = useState(width / height);

    useEffect(() => {
        setWidth(proposedPositionInstance.width);
        setHeight(proposedPositionInstance.height);
        setX(proposedPositionInstance.x);
        setY(proposedPositionInstance.y);
        setAspectRatio(proposedPositionInstance.width / proposedPositionInstance.height);
    }, [proposedPositionInstance]);

    const toggleConnect = () => {
        setIsConnected(!isConnected);
        setAspectRatio(width / height);
    };

    const updateDimensions = (newWidth, newHeight) => {
        proposedPositionInstance.editor.getEditableObjectsByType('singleElem', 'ProposedPosition')
            .forEach(editingObject => {
                editingObject.setWidth(newWidth);
                editingObject.setHeight(newHeight);
                proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                    editingObject.dbID,
                    {
                        bounds: editingObject.getBounds(),
                        size: {
                            height: newHeight,
                            width: newWidth
                        },
                        pos: {
                            x: editingObject.x,
                            y: editingObject.y
                        },
                        scaleX: editingObject.objectInside.scaleX,
                        scaleY: editingObject.objectInside.scaleY
                    }
                );
            });
    };

    const changeWidth = (width, save) => {
        width = parseInt(width);
        setWidth(width);

        if (isConnected) {
            const newHeight = Math.round(width / aspectRatio);
            setHeight(newHeight);
            if (save) {
                updateDimensions(width, newHeight);
            }
        } else {
            proposedPositionInstance.editor.getEditableObjectsByType('singleElem', 'ProposedPosition')
                .forEach(editingObject => {
                    editingObject.setWidth(width);
                    if (save) {
                        proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                            editingObject.dbID,
                            {
                                bounds: editingObject.getBounds(),
                                size: {
                                    height: height,
                                    width: width
                                },
                                pos: {
                                    x: editingObject.x,
                                    y: editingObject.y
                                },
                                scaleX: editingObject.objectInside.scaleX,
                                scaleY: editingObject.objectInside.scaleY
                            }
                        );
                    }
                });
        }
    };

    const changeHeight = (height, save) => {
        height = parseInt(height);
        setHeight(height);

        if (isConnected) {
            const newWidth = Math.round(height * aspectRatio);
            setWidth(newWidth);
            if (save) {
                updateDimensions(newWidth, height);
            }
        } else {
            proposedPositionInstance.editor.getEditableObjectsByType('singleElem', 'ProposedPosition')
                .forEach(editingObject => {
                    editingObject.setHeight(height);
                    if (save) {
                        proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                            editingObject.dbID,
                            {
                                bounds: editingObject.getBounds(),
                                size: {
                                    height: height,
                                    width: width
                                },
                                pos: {
                                    x: editingObject.x,
                                    y: editingObject.y
                                },
                                scaleX: editingObject.objectInside.scaleX,
                                scaleY: editingObject.objectInside.scaleY
                            }
                        );
                    }
                });
        }
    };

    const changeXPosition = (x, save) => {
        x = parseInt(x);
        proposedPositionInstance.editor.getEditableObjectsByType('singleElem', 'ProposedPosition')
            .forEach(editingObject => {
                editingObject.setPosition(x, editingObject.y);
                if (save) {
                    proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                        editingObject.dbID,
                        {
                            bounds: editingObject.getBounds(),
                            size: {
                                height: editingObject.trueHeight,
                                width: editingObject.trueWidth
                            },
                            pos: {
                                x: x,
                                y: editingObject.y
                            }
                        }
                    );
                }
            });
    };

    const changeYPosition = (y, save) => {
        y = parseInt(y);
        proposedPositionInstance.editor.getEditableObjectsByType('singleElem', 'ProposedPosition')
            .forEach(editingObject => {
                editingObject.setPosition(editingObject.x, y);
                if (save) {
                    proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                        editingObject.dbID,
                        {
                            bounds: editingObject.getBounds(),
                            size: {
                                height: editingObject.trueHeight,
                                width: editingObject.trueWidth
                            },
                            pos: {
                                x: editingObject.x,
                                y: y
                            }
                        }
                    );
                }
            });
    };

    return (
        <div className="dimensions-wrapper">
            <div className="width-height-container">
                <div className="height-box">
                    <span>W:</span>
                    <input 
                        type="number" 
                        className="height-input" 
                        value={height === 0 ? '' : parseInt(height)} 
                        onChange={(e) => {
                            const newHeight = Math.max(0, e.target.value);
                            changeHeight(newHeight, true);
                        }} 
                        onKeyDown={(e) => {
                            if (!/[0-9]/.test(e.key) && e.key !== 'Backspace' && e.key !== 'Tab') {
                                e.preventDefault();
                            }
                        }}
                        pattern="[0-9]*"
                    />
                </div>
                <div className="width-box">
                    <span>S:</span>
                    <input 
                        type="number" 
                        className="width-input" 
                        value={width === 0 ? '' : parseInt(width)} 
                        onChange={(e) => {
                            const newWidth = Math.max(0, e.target.value);
                            changeWidth(newWidth, true);
                        }} 
                        onKeyDown={(e) => {
                            if (!/[0-9]/.test(e.key) && e.key !== 'Backspace' && e.key !== 'Tab') {
                                e.preventDefault();
                            }
                        }}
                        pattern="[0-9]*"
                    />
                </div>
                <ConnectButton 
                    isConnected={isConnected}
                    toggleConnect={toggleConnect}
                />
            </div>
            <div className="width-height-container">
                <div className="height-box">
                    <span>X:</span>
                    <input 
                        type="number" 
                        className="height-input" 
                        value={parseInt(x)} 
                        onChange={(e) => {
                            setX(e.target.value);
                            changeXPosition(e.target.value, true);
                        }}
                        onKeyDown={(e) => {
                            if (!/[0-9]/.test(e.key) && e.key !== 'Backspace' && e.key !== 'Tab') {
                                e.preventDefault();
                            }
                        }}
                        pattern="[0-9]*" 
                    />
                </div>
                <div className="width-box">
                    <span>Y:</span>
                    <input 
                        type="number" 
                        className="width-input" 
                        value={parseInt(y)} 
                        onChange={(e) => {
                            setY(e.target.value);
                            changeYPosition(e.target.value, true);
                        }}
                        onKeyDown={(e) => {
                            if (!/[0-9]/.test(e.key) && e.key !== 'Backspace' && e.key !== 'Tab') {
                                e.preventDefault();
                            }
                        }}
                        pattern="[0-9]*" 
                    />
                </div>
            </div>
        </div>
    );
};

export default DimensionsWrapper;