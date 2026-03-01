import React from "react";
import ImagesButtons from "../../../buttons/ImagesButtonsList";

const ButtonsContainer = ({data, editor, loadFiles}) => {
    return (
        <div className={'buttons-wrapper'}>
            <div className={'buttons-container'}>
                <ImagesButtons.Components.Upload.Component uploadFunc={loadFiles}/>
                <ImagesButtons.Components.ChangeColumns.Component/>
            </div>
            <div className={'buttons-container'}>
                <ImagesButtons.Components.FillImagesAutomatically.Component editor={editor}
                                                                            disabled={data.isUploading}/>
                <div className={'assets-buttons-container'}>
                    <ImagesButtons.Components.UsedNotUsedImagesSwapper.Component data={data}/>
                    <ImagesButtons.Components.ReorderImages.Component editor={editor} disabled={data.isUploading}/>
                </div>
            </div>
        </div>
    )
}

export default ButtonsContainer