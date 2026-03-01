import React, {Component} from 'react'
import {connect} from 'react-redux'
import DeleteTool from "../DeleteTool";
import LayerUpTool from '../LayerUpTool'
import LayerDownTool from '../LayerDownTool'
import {selectBackFrameTool, selectBorderTool, selectEffectsTool, selectMaskTool, selectShadowTool} from "../../../redux/actions/proposedPositionToolbarActions";
import SizeTool from "./SizeTool";
import RotateTool from "./RotateTool";
import ZoomTool from "./ZoomTool";
import ImageToPageButton from "../../../components/canvasTools/ImageToPageButton";
import ImageToCenterButton from "../../../components/canvasTools/ImageToCenterButton";


class Toolbar extends Component {
    onLayerUpClick = (e) => {
        e.stopPropagation();

        const editingObject = this.props.proposedPositionInstance;

        const index = editingObject.parent.getChildIndex(editingObject);

        if (index < (editingObject.parent.children.length - 1)) {

            editingObject.parent.setChildIndex(editingObject, index + 1);
            editingObject.order = index + 1;

            const moveDownObject = editingObject.parent.getChildAt(index);
            moveDownObject.order = index;
            this.props.proposedPositionInstance.editor.webSocketControllers.userPage.moveObjectUp(this.props.proposedPositionInstance.dbID, this.props.proposedPositionInstance.getFirstImportantParent().userPage._id);
        }

    }

    onLayerDownClick = (e) => {
        e.stopPropagation();
        const editingObject = this.props.proposedPositionInstance;

        const index = editingObject.parent.getChildIndex(editingObject);

        if (index > 0) {

            editingObject.parent.setChildIndex(editingObject, index - 1);
            this.props.proposedPositionInstance.editor.webSocketControllers.userPage.moveObjectDown(this.props.proposedPositionInstance.dbID, this.props.proposedPositionInstance.getFirstImportantParent().userPage._id);

        }
        else if (editingObject.parent.name === 'foregroundLayer') {

            const background = editingObject.parent.parent.backgroundLayer;
            editingObject.parent.removeChild(editingObject);

            if (background.children.length > 0)
                background.addChildAt(editingObject, background.children.length - 1);
            else
                background.addChildAt(editingObject, background.children.length);

        }

    }

    onDeleteClick = () => {
        if (this.props.proposedPositionInstance.objectInside) {
            this.props.proposedPositionInstance.editor.webSocketControllers.proposedImage.removeObjectInside(
                this.props.proposedPositionInstance.parentPage.userPage._id,
                this.props.proposedPositionInstance.dbID)
        } else if (userType === 'advancedUser') {
            this.props.proposedPositionInstance.editor.webSocketControllers.userPage.removeProposedImage(
                this.props.proposedPositionInstance.getFirstImportantParent().userPage._id,
                this.props.proposedPositionInstance.dbID
            )
        }
    }

    // those methods might be useful
    imageToPage = (e) => {
        e.stopPropagation();
        this.props.proposedPositionInstance.objectInside.setFullSize2();
        this.props.proposedPositionInstance.editor.tools.init();
    }

    imageToCenter = (e) => {
        e.stopPropagation();
        this.props.proposedPositionInstance.editorBitmapInstance.center();
        this.editor.tools.init();
    }

    render() {
        return (
            <div className="simple editor-bitmap-tools">
                <DeleteTool onClick={this.onDeleteClick}/>
                {this.props.advanced && (
                    <>
                        <LayerUpTool onClick={this.onLayerUpClick}/>
                        <LayerDownTool onClick={this.onLayerDownClick}/>
                        {/*<ImageToPageButton onClick={(e) => this.imageToPage(e)}/>*/}
                        {/*<ImageToCenterButton onClick={(e) => this.imageToCenter(e)}/>*/}
                        <button className={'bitmap-tool-button lock'}></button>
                    </>
                )}
            </div>
        )
    }
}

Toolbar.propTypes = {}
const mapStateToProps = (state) => {
    return {
        proposedPositionToolbar: state.proposedPositionToolbar
    }
}
const mapDispatchToProps = (dispatch) => {
    return {
        onBackFrameClick: (select) => {
            dispatch(selectBackFrameTool(select))
        },
        onBorderClick: (select) => {
            dispatch(selectBorderTool(select))
        },
        onEffectsClick: (select) => {
            dispatch(selectEffectsTool(select))
        },
        onMaskClick: (select) => {
            dispatch(selectMaskTool(select))
        },
        onShadowClick: (select) => {
            dispatch(selectShadowTool(select))
        },

    }
}
export default connect(mapStateToProps, mapDispatchToProps)(Toolbar)
