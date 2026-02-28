import React from 'react'
import RangeOptions from './RangeOptions';

const MasksContent = () => {

    const onSwitchChange = (checked) => {
        const props = {maskFilter: checked ? maskId : null}
        const maskAsset = editor.userProject.findMaskById(maskId)
        editor.getEditableObjectsByType(state.range, 'ProposedPosition')
            .forEach(editingObject => {
                    if (checked) {
                        if (maskAsset) {
                            editingObject.addImageAlphaFilter(maskAsset)
                        }
                    }
                    else {
                        editingObject.removeAlphaMask()
                    }
                    editor.webSocketControllers.proposedImage.setAttributes(
                        editingObject.dbID, props
                    )
                }
            )
    }

    const onFrameClick = (maskId) => {
        maskId = maskId
        onSwitchChange(true)
    }

    return (
        <>
            <div className='masks-container'>
                <RangeOptions text='Opcje maski dla zdjęcia:'/>
            </div>
        </>
    )
}

export default MasksContent;