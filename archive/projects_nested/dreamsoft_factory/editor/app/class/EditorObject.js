var _ = require('lodash');

// Depending on the environment (user or admin), require the appropriate EditorObject extension
var EditorObject_extend = EDITOR_ENV.user
    ? require('./EditorObject_user').EditorObject_user
    : require('./EditorObject_admin').EditorObject_admin;

import EditorShadow2 from './EditorShadow2';

// import {LeftMagneticRuler} from './LeftMagneticRuler'; // Uncomment if needed

/**
 * Class representing an object in the Editor.
 *
 * @class EditorObject
 * @constructor
 * @param {Boolean} initEvents - Whether to initialize events
 * @param {Object} settings - Configuration settings for the object
 * @param {Object} container - Optional container for the object
 */
function EditorObject(initEvents, settings, container) {
    var that = this;
    var settings = settings || {};

    // Call the Container constructor from createjs
    createjs.Container.call(this);

    // Initialize properties
    this.tools;
    this.isBlocked = false;
    this.type = null;
    this.rotation = settings.rotation || 0;
    this.trueWidth = this.width = settings.width || 10;
    this.trueHeight = this.height = settings.height || 10;
    this.scaleX = settings.scaleX || 1;
    this.scaleY = settings.scaleY || 1;
    this.dbID = settings.dbID;
    this.dbId = settings.dbID;
    this.shadowBlur = settings.shadowBlur || 5;
    this.shadowColor = settings.shadowColor || 'rgba(0,0,0,255)';
    this.shadowOffsetX = settings.shadowOffsetX || 0;
    this.shadowOffsetY = settings.shadowOffsetY || 0;
    this.dropShadow = settings.dropShadow || false;
    this.displaySimpleBorder = settings.displaySimpleBorder || false;
    this.borderColor = settings.borderColor || '#000';
    this.borderWidth = settings.borderWidth || 0;
    this.backgroundFrameID = settings.backgroundFrameID || null;
    this.backgroundFrame = this.backgroundFrameID != null;
    this.name = name;
    this.snapToPixel = true;
    this.uid = null;
    this.toolsBox = null;
    this.x = settings.x || 0;
    this.y = settings.y || 0;
    this.layerElement = null;

    this.moveVector = {
        start: null,
        stop: null,
    };

    // If no container is provided, add custom shadow
    if (!container) {
        this.addChild(this.customShadow);
    }

    // Create layers for border, main content, shadow, and background frame
    this.borderLayer = new createjs.Container();
    this.mainLayer = new createjs.Container();
    this.shadowLayer = new createjs.Container();
    this.backgroundFrameLayer = new createjs.Container();

    // Add layers to the object
    this.addChild(this.shadowLayer);
    this.addChild(this.backgroundFrameLayer);
    this.addChild(this.mainLayer);

    // Initialize simple border shape
    this.simpleBorder = new createjs.Shape();
    this.updateSimpleBorder();
    this.simpleBorder.visible = this.displaySimpleBorder;

    // Update shadow based on settings
    this.updateShadow();

    this.history_tmp;

    // Initialize events if required
    if (initEvents) {
        this.initEvents();
    }

    // Add event listener for 'destroyBitmap' event
    this.addEventListener('destroyBitmap', function (e) {
        // Handle bitmap destruction
        // alert('destroyBitmap: ' + e.uid );
    });

    // Add simple border to the object if applicable
    if (this.simpleBorder && !container) {
        this.addChild(this.simpleBorder);
    }

    // Add border layer
    this.addChild(this.borderLayer);
}

// Extend the prototype of EditorObject
var p = (EditorObject.prototype = $.extend(
    true,
    {},
    new Object(createjs.Container.prototype),
    new Object(EditorObject_extend.prototype)
));

p.constructor = EditorObject;

/**
 * Reset object settings to default values
 *
 * @method defaultSettings
 */
p.defaultSettings = function () {
    // If drop shadow is enabled, remove it
    if (this.dropShadow) {
        this.unDropShadow();
    }

    // If simple border is displayed, remove it
    if (this.displaySimpleBorder) {
        this.unDropBorder();
    }
};

/**
 * Set the border width of the object
 *
 * @method setBorderWidth
 * @param {Number} width - New border width
 * @param {Boolean} save - Whether to save the change to the server
 */
p.setBorderWidth = function (width, save) {
    this.borderWidth = width;

    // If width is greater than 0, display border; otherwise, hide it
    width > 0 ? this.dropBorder() : this.unDropBorder();

    // Save the change if required
    if (save) {
        this.editor.webSocketControllers[this.socketController].setAttributes(
            this.dbID,
            this.editor.adminProject.format.view.getId(),
            {
                borderWidth: width,
            }
        );
    }
};

/**
 * Update the object's transformation in the database
 *
 * @method updateTransformInDB
 */
p.updateTransformInDB = function () {
    this.editor.webSocketControllers[this.socketController].setTransform(
        this.x,
        this.y,
        this.rotation,
        this.scaleX,
        this.scaleY,
        this.dbID
    );
};

/**
 * Set the rotation of the object
 *
 * @method setRotation
 * @param {Number} rotation - New rotation value
 */
p.setRotation = function (rotation) {
    this.rotation = rotation;

    // Update mask rotation if mask exists
    if (this.mask) {
        this.mask.rotation = parseInt(rotation);
    }
};

/**
 * Set the rotation value and optionally save it
 *
 * @method setRotationValue
 * @param {Number} rotation - New rotation value
 * @param {Boolean} save - Whether to save the change
 */
p.setRotationValue = function (rotation, save) {
    this.tempRotation = rotation;

    if (save) {
        this.editor.webSocketControllers[this.socketController].setAttributes(
            this.dbID,
            this.editor.adminProject.format.view.getId(),
            {
                rotation: rotation,
            }
        );
    }
};

/**
 * Remove drop shadow from the object
 *
 * @method unDropShadow
 * @param {Boolean} save - Whether to save the change
 */
p.unDropShadow = function (save) {
    this.shadowLayer.removeChild(this.customShadow);
    this.customShadow = null;
    this.dropShadow = false;

    // Uncomment and adjust if saving functionality is needed
    /*
    if (save) {
      this.editor.webSocketControllers[this.socketController].setAttributes(
        this.dbID,
        this.editor.adminProject.format.view.getId(),
        {this.props.proposedPositionInstance.editorBitmapInstance
          dropShadow: false,
        }
      );
    }
    */
};

/**
 * Display the border around the object
 *
 * @method dropBorder
 */
p.dropBorder = function () {
    this.displaySimpleBorder = this.simpleBorder.visible = true;
};

/**
 * Hide the border around the object
 *
 * @method unDropBorder
 */
p.unDropBorder = function () {
    this.displaySimpleBorder = this.simpleBorder.visible = false;
};

/**
 * Set the shadow blur amount
 *
 * @method setShadowBlur
 * @param {Number} blur - Blur amount
 * @param {Boolean} save - Whether to save the change
 */
p.setShadowBlur = function (blur, save) {
    this.shadowBlur = blur;
    // Update shadow if necessary

    if (save) {
        this.editor.webSocketControllers[this.socketController].setAttributes(
            this.dbID,
            this.editor.adminProject.format.view.getId(),
            {
                shadowBlur: blur,
            }
        );
    }
};

/**
 * Set the shadow color
 *
 * @method setShadowColor
 * @param {String} color - New shadow color
 * @param {Boolean} save - Whether to save the change
 */
p.setShadowColor = function (color, save) {
    this.shadowColor = color;
    // Update shadow if necessary

    if (save) {
        this.editor.webSocketControllers[this.socketController].setAttributes(
            this.dbID,
            this.editor.adminProject.format.view.getId(),
            {
                shadowColor: color,
            }
        );
    }
};

/**
 * Set the horizontal offset of the shadow
 *
 * @method setShadowOffsetX
 * @param {Number} posX - New horizontal offset
 * @param {Boolean} save - Whether to save the change
 */
p.setShadowOffsetX = function (posX, save) {
    this.shadowOffsetX = posX;
    // Update shadow offset if necessary

    if (save) {
        this.editor.webSocketControllers[this.socketController].setAttributes(
            this.dbID,
            this.editor.adminProject.format.view.getId(),
            {
                shadowOffsetX: posX,
            }
        );
    }
};

/**
 * Set the vertical offset of the shadow
 *
 * @method setShadowOffsetY
 * @param {Number} posY - New vertical offset
 * @param {Boolean} save - Whether to save the change
 */
p.setShadowOffsetY = function (posY, save) {
    this.shadowOffsetY = posY;
    // Update shadow offset if necessary

    if (save) {
        this.editor.webSocketControllers[this.socketController].setAttributes(
            this.dbID,
            this.editor.adminProject.format.view.getId(),
            {
                shadowOffsetY: posY,
            }
        );
    }
};

/**
 * Update the shadow effect based on current properties
 *
 * @method updateShadow
 */
p.updateShadow = function () {
    if (this.customShadow) {
        this.customShadow.updateShadow(
            this,
            this.shadowBlur,
            this.shadowColor,
            this.shadowOffsetX,
            this.shadowOffsetY
        );
    }
};

/**
 * Set the border color and optionally save it
 *
 * @method setBorderColor
 * @param {String} color - New border color
 * @param {Boolean} save - Whether to save the change
 */
p.setBorderColor = function (color, save) {
    this.borderColor = color;
    this.updateSimpleBorder();

    if (save) {
        this.editor.webSocketControllers[this.socketController].setAttributes(
            this.dbID,
            this.editor.adminProject.format.view.getId(),
            {
                borderColor: color,
            }
        );
    }
};

/**
 * Add a drop shadow effect to the object
 *
 * @method dropShadowAdd
 * @param {Boolean} save - Whether to save the change
 */
p.dropShadowAdd = function (save) {
    var Editor = this.editor;

    if (this.dropShadow == false) {
        this.customShadow = new EditorShadow2(
            this,
            this.shadowBlur,
            this.shadowColor,
            this.shadowOffsetX,
            this.shadowOffsetY,
            4
        );
        this.shadowLayer.addChildAt(this.customShadow, 0);
        this.dropShadow = true;
    }

    if (save) {
        this.editor.webSocketControllers[this.socketController].setAttributes(
            this.dbID,
            this.editor.adminProject.format.view.getId(),
            {
                dropShadow: true,
            }
        );
    }
};

/**
 * Update the simple border graphics based on current properties
 *
 * @method updateSimpleBorder
 */
p.updateSimpleBorder = function () {
    this.simpleBorder.graphics
        .c()
        .f(this.borderColor)
        .r(0, 0, this.width - this.borderWidth / this.scaleX, this.borderWidth / this.scaleY)
        .r(
            this.width - this.borderWidth / this.scaleX,
            0,
            this.borderWidth / this.scaleX,
            this.height - this.borderWidth / this.scaleY
        )
        .r(
            this.borderWidth / this.scaleX,
            this.height - this.borderWidth / this.scaleY,
            this.width - this.borderWidth / this.scaleX,
            this.borderWidth / this.scaleY
        )
        .r(
            0,
            this.borderWidth / this.scaleY,
            this.borderWidth / this.scaleX,
            this.height - this.borderWidth / this.scaleY
        );

    if (this.dropShadow) {
        this.updateShadow();
    }
};

/**
 * Get the true scale of the object, considering parent scales
 *
 * @method getTrueScale
 * @return {Object} - Object containing x and y scales
 */
p.getTrueScale = function () {
    var scaleX = 1;
    var scaleY = 1;

    var parent = this;

    // Traverse up the parent chain and multiply scales
    while (parent) {
        scaleX *= parent.scaleX;
        scaleY *= parent.scaleY;
        parent = parent.parent;

        // Stop if no more parents
        if (!parent.parent) parent = parent.parent;
    }

    return {
        x: scaleX,
        y: scaleY,
    };
};

/**
 * Get the true rotation of the object, considering parent rotations
 *
 * @method getTrueRotation
 * @return {Number} - The cumulative rotation
 */
p.getTrueRotation = function () {
    var rotation = 0;

    var parent = this;

    // Traverse up the parent chain and sum rotations
    while (parent) {
        rotation += parent.rotation;
        parent = parent.parent;
    }

    return rotation;
};

/**
 * Update magnetic lines (alignment guides) based on object's position TODO: Implement functionality
 *
 * @method updateMagneticLines
 */
p.updateMagneticLines = function () {
    return;

    if (this.magneticLines) {
        var bounds = this.getGlobalTransformedBounds();

        this.magneticLines.vertical.left.x = bounds.x;
        this.magneticLines.vertical.right.x = bounds.x + bounds.width;
        this.magneticLines.vertical.center.x = bounds.x + bounds.width / 2;
        this.magneticLines.horizontal.top.y = bounds.y;
        this.magneticLines.horizontal.bottom.y = bounds.y + bounds.height;
        this.magneticLines.horizontal.center.y = bounds.y + bounds.height / 2;
    }
};

/**
 * Check for alignment with other objects using magnetic lines
 *
 * @method checkMagneticLines
 * @param {Boolean} left - Check left alignment
 * @param {Boolean} centerVertical - Check vertical center alignment
 * @param {Boolean} right - Check right alignment
 * @param {Boolean} top - Check top alignment
 * @param {Boolean} bottom - Check bottom alignment
 * @param {Boolean} centerHorizontal - Check horizontal center alignment
 */
p.checkMagneticLines = function (
    left,
    centerVertical,
    right,
    top,
    bottom,
    centerHorizontal
) {
    if (this.magneticLines) {
        // Update visibility and closest lines based on parameters
        if (centerHorizontal) {
            this.magneticLines.horizontal.center.getClosestLine();
        } else {
            this.magneticLines.horizontal.center.visible = false;
            this.magneticLines.horizontal.center.closestLine = null;
        }

        if (left) {
            this.magneticLines.vertical.left.getClosestLine();
        } else {
            this.magneticLines.vertical.left.visible = false;
            this.magneticLines.vertical.left.closestLine = null;
        }

        if (centerVertical) {
            this.magneticLines.vertical.center.getClosestLine();
        } else {
            this.magneticLines.vertical.center.visible = false;
            this.magneticLines.vertical.center.closestLine = null;
        }

        if (right) {
            this.magneticLines.vertical.right.getClosestLine();
        } else {
            this.magneticLines.vertical.right.visible = false;
            this.magneticLines.vertical.right.closestLine = null;
        }

        if (top) {
            this.magneticLines.horizontal.top.getClosestLine();
        } else {
            this.magneticLines.horizontal.top.visible = false;
            this.magneticLines.horizontal.top.closestLine = null;
        }

        if (bottom) {
            this.magneticLines.horizontal.bottom.getClosestLine();
        } else {
            this.magneticLines.horizontal.bottom.visible = false;
            this.magneticLines.horizontal.bottom.closestLine = null;
        }

        var closestVerticalAlign = null;
        var closestHorizontalAlign = null;

        // Find the closest vertical alignment line
        for (var line in this.magneticLines.vertical) {
            var line = this.magneticLines.vertical[line];

            if (closestVerticalAlign && line.closestLine) {
                if (
                    Math.abs(closestVerticalAlign.x - closestVerticalAlign.closestLine.x) >
                    Math.abs(line.x - line.closestLine.x)
                ) {
                    closestVerticalAlign = line;
                }
            } else if (line.closestLine) {
                closestVerticalAlign = line;
            }
        }

        if (closestVerticalAlign) closestVerticalAlign.magnetizeObject();

        // Find the closest horizontal alignment line
        for (var line in this.magneticLines.horizontal) {
            var line = this.magneticLines.horizontal[line];

            if (closestHorizontalAlign && line.closestLine) {
                if (
                    Math.abs(closestHorizontalAlign.y - closestHorizontalAlign.closestLine.y) >
                    Math.abs(line.y - line.closestLine.y)
                ) {
                    closestHorizontalAlign.visible = closestHorizontalAlign.closestLine.visible = false;
                    closestHorizontalAlign = line;
                }
            } else if (line.closestLine) {
                closestHorizontalAlign = line;
            }
        }

        if (closestHorizontalAlign) closestHorizontalAlign.magnetizeObject();
    }
};

/**
 * Get the bounds of the object relative to the window (canvas)
 *
 * @method getWindowsBounds
 * @return {Object} - The bounds with scaled width and height
 */
p.getWindowsBounds = function () {
    var bounds = this.getGlobalTransformedBounds();
    bounds.width = bounds.width * this.editor.getStage().scaleX;
    bounds.height = bounds.height * this.editor.getStage().scaleY;

    return bounds;
};

/**
 * Multiply the current scale by a given value
 *
 * @method multiplyScaleBy
 * @param {Number} multiplyValue - The value to multiply the scale by
 */
p.multiplyScaleBy = function (multiplyValue) {
    this.scaleX *= multiplyValue;
    this.scaleY *= multiplyValue;

    this.width = this.trueWidth * this.scaleX;
    this.height = this.trueHeight * this.scaleY;
};

/**
 * Zoom the object to fit the screen
 *
 * @method getRealScale
 * @return {Object} - Object containing new scale values
 */
p.getRealScale = function () {
    var scaleX = 1;
    var scaleY = 1;

    var tmpX = this.editor.getStage().scaleX;
    var tmpY = this.editor.getStage().scaleY;

    var parent = this;

    // Traverse up the parent chain and multiply scales
    while (parent) {
        scaleX *= parent.scaleX;
        scaleY *= parent.scaleY;
        parent = parent.parent;

        // Stop if no more parents
        if (!parent.parent) parent = parent.parent;
    }

    var offset = 80;
    var destinationMaxWidth = this.editor.getCanvas().width() - offset;
    var destinationMaxHeight = this.editor.getCanvas().height() - offset;
    var maxSize = destinationMaxHeight;

    var maxHeight = destinationMaxHeight;
    var maxWidth = destinationMaxWidth;

    var windowPosition = {
        x: (this.editor.getCanvas().width() - maxSize) / 2,
        y: (this.editor.getCanvas().height() - maxSize) / 2,
    };

    var that = this;

    var test = maxSize / (that.trueHeight * scaleX) / 50 + tmpX;

    var posG = this.localToLocal(this.regX, this.regY, this.editor.getStage());

    var vector = {
        x: this.editor.getStage().x - posG.x * this.editor.getStage().scaleX,
        y: this.editor.getStage().y - posG.y,
    };

    posTemp = posG.x / 50;

    var stageStart = this.editor.getStage().x / this.editor.getStage().scaleX;

    var vector = {
        x: this.editor.getStage().x - posG.x * this.editor.getStage().scaleX,
        y: this.editor.getStage().y - posG.y * this.editor.getStage().scaleX,
    };

    // The following code handles the zoom animation (omitted for brevity)
    // ...

    var pos = Editor.stage.getMousePosition(windowPosition.x, windowPosition.y);

    return { sx: scaleX, sy: scaleY };
};

/**
 * Show magnetic lines based on parameters
 *
 * @method showMagneticLines
 * @param {Boolean} top - Show top line
 * @param {Boolean} bottom - Show bottom line
 * @param {Boolean} left - Show left line
 * @param {Boolean} right - Show right line
 * @param {Boolean} center - Show center vertical line
 * @param {Boolean} centerHorizontal - Show center horizontal line
 */
p.showMagneticLines = function (top, bottom, left, right, center, centerHorizontal) {
    return;

    if (this.magneticLines) {
        this.magneticLines.vertical.right.visible = !!right;
        this.magneticLines.vertical.left.visible = !!left;
        this.magneticLines.horizontal.bottom.visible = !!bottom;
        this.magneticLines.horizontal.top.visible = !!top;
        this.magneticLines.vertical.center.visible = !!center;
        this.magneticLines.horizontal.center.visible = !!centerHorizontal;
    }
};

/**
 * Move the object by a given vector
 *
 * @method moveByVector
 * @param {Array} vector - [x, y] movement vector
 */
p.moveByVector = function (vector) {
    this.x += vector[0];
    this.y += vector[1];

    if (this.mask) {
        this.mask.x += vector[0];
        this.mask.y += vector[1];
    }
};

/**
 * Set the width of the object (adjusts scale)
 *
 * @method setWidth
 * @param {Number} w - New width
 */
p.setWidth = function (w) {
    this.scaleX = (1 / this.width) * w;

    if (this.mask) {
        this.mask.scaleX = (1 / this.width) * w;
    }

    if (this.updateSimpleBorder) {
        this.updateSimpleBorder();
    }
};

/**
 * Set the height of the object (adjusts scale)
 *
 * @method setHeight
 * @param {Number} h - New height
 */
p.setHeight = function (h) {
    this.scaleY = (1 / this.height) * h;

    if (this.mask) {
        this.mask.scaleY = (1 / this.height) * h;
    }

    if (this.updateSimpleBorder) {
        this.updateSimpleBorder();
    }
};

/**
 * Set the true width of the object without changing scale
 *
 * @method setTrueWidth
 * @param {Number} w - New true width
 * @param {Boolean} blockLeftCornerPosition - Whether to keep the left corner position
 */
p.setTrueWidth = function (w, blockLeftCornerPosition) {
    var widthBefore = this.width;

    this.trueWidth = w;
    this.width = w * this.scaleX;
    this.regX = w / 2;

    if (this.mask) {
        this.mask.regX = this.regX;
    }

    if (blockLeftCornerPosition) {
        var vector = (this.width - widthBefore) / 2;
        this.x += vector;
    }
};

/**
 * Get the editable siblings of the object
 *
 * @method getEditableSiblings
 */
p.getEditableSiblings = function () {
    var allSiblings = this.getFirstImportantParent().children;

    var siblingsArray = [];

    for (var i = 0; i < allSiblings.length; i++) {
        if (allSiblings[i] instanceof Layer || allSiblings[i] instanceof EditableArea) {
            // Skip layers and editable areas
        } else {
            siblingsArray.push(allSiblings[i]);
        }
    }
};

/**
 * Get the first parent that is considered important
 *
 * @method getFirstImportantParent
 * @return {Object} - The important parent object
 */
p.getFirstImportantParent = function () {
    let parent = this.parent;
    while (parent) {
        if (this.editor.importantParents) {
            for (var i = 0; i < this.editor.importantParents.length; i++) {
                if (parent instanceof this.editor.importantParents[i]) return parent;
            }
        }
        parent = parent.parent;
    }
};

/**
 * Set the true height of the object without changing scale
 *
 * @method setTrueHeight
 * @param {Number} h - New true height
 * @param {Boolean} blockLeftCornerPosition - Whether to keep the left corner position
 */
p.setTrueHeight = function (h, blockLeftCornerPosition) {
    var heightBefore = this.height;

    this.trueHeight = h;
    this.height = h * this.scaleX;
    this.regY = h / 2;

    if (this.mask) {
        this.mask.regY = this.regY;
    }

    if (blockLeftCornerPosition) {
        var vector = (this.height - heightBefore) / 2;
        this.y -= vector;
    }
};

/**
 * Move the object to the tools layer for editing
 *
 * @method moveToToolsLayer
 * @param {Function} callback - Optional callback function
 */
p.moveToToolsLayer = function (callback) {
    // Save current position and parent information
    this.xBefore = this.x;
    this.yBefore = this.y;
    this.orderBefore = this.parent.getChildIndex(this);
    this.parentBefore = this.parent;
    this.parentPage = this.getFirstImportantParent();

    // Convert local position to global position
    var loc = this.parent.localToLocal(this.x, this.y, this.editor.getStage());
    this.x = loc.x;
    this.y = loc.y;

    if (this.mask) {
        this.mask.x = loc.x;
        this.mask.y = loc.y;
    }

    // Add object to the tools layer
    this.editor.stage.getToolsLayer().addChild(this);
};

/**
 * Move the object back from the tools layer to its original position
 *
 * @method backFromToolsLayer
 * @param {Boolean} position - Whether to restore the original position
 */
p.backFromToolsLayer = function (position) {
    if (position) {
        this.x = this.xBefore;
        this.y = this.yBefore;

        if (this.mask) {
            this.mask.x = this.xBefore;
            this.mask.y = this.yBefore;
        }
    }

    // Add object back to its original parent at the original index
    this.parentBefore.addChildAt(this, this.orderBefore);
    this.parentBefore = null;
};

/**
 * Set the scale of the object
 *
 * @method setScale
 * @param {Number} scaleValue - New scale value
 */
p.setScale = function (scaleValue) {
    this.scaleX = this.scaleY = scaleValue;
    this.width = this.trueWidth * scaleValue;
    this.height = this.trueHeight * scaleValue;
};

/**
 * Set the object to full size relative to its parent
 *
 * @method setFullSize
 */
p.setFullSize = function () {
    var widthTo = this.parent.trueWidth;
    var heightTo = this.parent.trueHeight;

    if (this.rotation % 180 != 90) {
        if (this.width < this.parent.width) {
            var scaleValue = widthTo / this.trueWidth;

            this.scaleX = scaleValue;
            this.scaleY = scaleValue;
            this.width = this.trueWidth * scaleValue;
            this.height = this.trueHeight * scaleValue;
        } else if (this.height < this.parent.height) {
            var scaleValue = heightTo / this.trueHeight;
            this.scaleX = scaleValue;
            this.scaleY = scaleValue;
            this.width = this.trueWidth * scaleValue;
            this.height = this.trueHeight * scaleValue;
        }
    } else {
        if (this.width < this.parent.height) {
            var scaleValue = heightTo / this.trueWidth;

            this.scaleX = scaleValue;
            this.scaleY = scaleValue;
            this.width = this.trueWidth * scaleValue;
            this.height = this.trueHeight * scaleValue;
        } else if (this.height < this.parent.width) {
            var scaleValue = widthTo / this.trueHeight;

            this.scaleX = scaleValue;
            this.scaleY = scaleValue;
            this.width = this.trueWidth * scaleValue;
            this.height = this.trueHeight * scaleValue;
        }
    }
};

/**
 * Another method to set the object to full size relative to its parent
 *
 * @method setFullSize2
 */
p.setFullSize2 = function () {
    var widthTo = this.parent.width;
    var heightTo = this.parent.height;

    var scaleValue = this.width > this.height ? widthTo / this.width : heightTo / this.height;

    this.scaleX = scaleValue;
    this.scaleY = scaleValue;

    if (this.width * this.scaleX < this.parent.width) {
        scaleValue = widthTo / this.width;

        this.scaleX = scaleValue;
        this.scaleY = scaleValue;
    } else if (this.height * this.scaleY < this.parent.height) {
        scaleValue = heightTo / this.height;
        this.scaleX = scaleValue;
        this.scaleY = scaleValue;
    }
};

/**
 * Get the history element for transformations
 *
 * @method getHistoryElem
 * @param {Object} elem - Element to retrieve
 * @return {Object} - The history element
 */
p.getHistoryElem = function (elem) {
    return this.history_tmp;
};

/**
 * Rotate the object by a given angle
 *
 * @method rotate
 * @param {Number} rotation - Rotation angle in degrees
 */
p.rotate = function (rotation) {
    var editing_id = this.editor.tools.getEditObject();
    var editingObject = this.editor.stage.getObjectById(editing_id);

    this.rotation += rotation || 0;

    try {
        document.getElementById('setRotationInput').value = parseInt(
            editingObject.rotation % 360
        ).toFixed(0);
    } catch (e) {}

    if (this.mask) {
        this.mask.rotation += rotation;
    }

    if (this.reactChange) {
        this.reactChange();
    }
};

/**
 * Set the position of the object
 *
 * @method setPosition
 * @param {Number} x - New x-coordinate
 * @param {Number} y - New y-coordinate
 */
p.setPosition = function (x, y) {
    this.x = x;
    this.y = y;

    if (this.mask) {
        this.mask.x = x;
        this.mask.y = y;
    }

    if (this.contextMenu) {
        this.contextMenu._updateToolsBoxPosition();
    }
};

/**
 * Set the position of the object based on the top-left corner
 *
 * @method setPosition_leftCorner
 * @param {Number} x - New x-coordinate
 * @param {Number} y - New y-coordinate
 */
p.setPosition_leftCorner = function (x, y) {
    var bounds = this.getTransformedBounds();

    bounds = bounds || { width: 0, height: 0 };

    this.x = x + bounds.width / 2;
    this.y = y + bounds.height / 2;

    if (this.mask) {
        this.mask.x = x + bounds.width / 2;
        this.mask.y = y + bounds.height / 2;
    }
};

/**
 * Toggle the visibility of the object
 *
 * @method toggleVisible
 */
p.toggleVisible = function () {
    this.visible = !this.visible;
};

/**
 * Toggle the event blocking of the object
 *
 * @method toggleLock
 */
p.toggleLock = function () {
    this.mouseEnabled = !this.mouseEnabled;
};

/**
 * Set the registration point (rotation point) to the center
 *
 * @method setCenterReg
 */
p.setCenterReg = function () {
    if (this.regX == 0 || !this.regX) {
        this.regX = this.trueWidth / 2;
        this.regY = this.trueHeight / 2;
        var pos = this.localToLocal(this.trueWidth, this.trueHeight, this.parent);
        this.x = pos.x;
        this.y = pos.y;

        if (this.mask) {
            this.mask.x = pos.x;
            this.mask.y = pos.y;
            this.mask.regX = this.trueWidth / 2;
            this.mask.regY = this.trueHeight / 2;
        }
    }
};

/**
 * Center the object relative to its parent
 *
 * @method center
 */
p.center = function () {
    var parent = this.parent;

    this.x = parent.width / 2;
    this.y = parent.height / 2;

    if (this.mask) {
        this.mask.x = this.x;
        this.mask.y = this.y;
    }
};

/**
 * Center the object horizontally relative to its parent
 *
 * @method centerX
 */
p.centerX = function () {
    var parent = this.parent;
    this.x = parent.width / 2;
};

/**
 * Center the object vertically relative to its parent
 *
 * @method centerY
 */
p.centerY = function () {
    var parent = this.parent;
    this.y = parent.height / 2;
};

/**
 * Custom hit test function
 *
 * @method customHitTest
 * @param {Number} stageX - X-coordinate on the stage
 * @param {Number} stageY - Y-coordinate on the stage
 */
p.customHitTest = function (stageX, stageY) {
    this.globalToLocal(stageX, stageY);
};

/**
 * Generate HTML representation for layer panel
 *
 * @method toLayerHTML
 * @return {HTMLElement} - The HTML element representing the object
 */
p.toLayerHTML = function () {
    var _this = this;

    var layerElem = document.createElement('li');
    layerElem.addEventListener('click', function (e) {
        e.stopPropagation();
    });

    var layerVisibility = document.createElement('span');
    layerVisibility.className =
        'objectVisibility ' + (this.visible ? 'visible' : 'notvisible');

    layerVisibility.addEventListener('click', function (e) {
        e.stopPropagation();

        _this.visible = !_this.visible;
        layerVisibility.className =
            'objectVisibility ' + (_this.visible ? 'visible' : 'notvisible');
    });

    var layerElemTitle = document.createElement('span');
    layerElemTitle.className = 'objectName';
    layerElemTitle.innerHTML = this.name;
    layerElem.appendChild(layerVisibility);
    layerElem.appendChild(layerElemTitle);

    return layerElem;
};

/**
 * Set the global position of the object
 *
 * @method setGlobalPosition
 * @param {Number} x - New global x-coordinate
 * @param {Number} y - New global y-coordinate
 */
p.setGlobalPosition = function (x, y) {
    var pos = this.globalToLocal(x, y, this.parent);
    this.x = pos.x;
    this.y = pos.y;
};

/**
 * Get the global position of the object
 *
 * @method getGlobalPosition
 * @return {Array} - [x, y] coordinates
 */
p.getGlobalPosition = function () {
    var x,
        y = 0;
    var main = this.editor.stage.getObjectById(MAIN_LAYER);

    var pos = this.localToGlobal(this.regX, this.regY);

    x = pos.x;
    y = pos.y;

    return [x, y];
};

/**
 * Get the position of the top-left corner of the object
 *
 * @method getLeftTopCornerPosition
 * @return {Array} - [x, y] coordinates
 */
p.getLeftTopCornerPosition = function () {
    return [this.x - this.trueWidth / 2, this.y - this.trueHeight / 2];
};

/**
 * Save the object's transformation in the database
 *
 * @method saveTransformation
 */
p.saveTransformation = function () {
    var o = this;
    var obj = this;

    var transformations = {
        rotation: o.rotation,
        x: o.x,
        y: o.y,
        sX: o.scaleX,
        sY: o.scaleY,
        tw: obj.trueWidth,
        th: obj.trueHeight,
        w: obj.width,
        h: obj.height,
        rX: o.regX,
        rY: o.regY,
    };

    obj.updateInDB('matrix', JSON.stringify(transformations));
};

/**
 * Update an attribute in the database
 *
 * @method updateInDB
 * @param {String} key - Attribute key
 * @param {String} value - Attribute value
 */
p.updateInDB = function (key, value) {
    var project_id = this.editor.getProjectId();

    var layer_id = this.editor.stage.getObjectById(this.id).dbId;

    $.ajax({
        url:
            'https://api.digitalprint9.pro/adminProjects/' +
            project_id +
            '/adminProjectLayers/' +
            layer_id +
            '/adminProjectObjects/' +
            this.dbId,
        type: 'POST',
        headers: {
            'x-http-method-override': 'patch',
        },
        crossDomain: true,
        contentType: 'application/json',
        data: '{ "' + key + '" : ' + value + '}',
        success: function (data) {
            // Handle success
        },
        error: function (data) {
            // Handle error
        },
    });
};

/**
 * Check if the object is in an editable area (only for administrators)
 *
 * @method isInEditableArea
 * @return {Boolean} - True if in editable area
 */
p.isInEditableArea = function () {
    var parent = this.parent;

    while (parent) {
        if (parent instanceof EditableArea) return true;

        parent = parent.parent;
    }

    return false;
};

/**
 * Remove magnetic lines from the object
 *
 * @method removeMagneticLines
 */
p.removeMagneticLines = function () {
    // Remove magnetic lines if they exist
    /*
    this.magneticLines.vertical.left.parent.removeChild(this.magneticLines.vertical.left);
    this.magneticLines.vertical.right.parent.removeChild(this.magneticLines.vertical.right);
    this.magneticLines.vertical.center.parent.removeChild(this.magneticLines.vertical.center);
    this.magneticLines.horizontal.top.parent.removeChild(this.magneticLines.horizontal.top);
    this.magneticLines.horizontal.bottom.parent.removeChild(this.magneticLines.horizontal.bottom);
    this.magneticLines.horizontal.center.parent.removeChild(this.magneticLines.horizontal.center);
    */
};

/**
 * Prepare magnetic lines for alignment
 *
 * @method prepareMagneticLines
 * @param {Number} tolerance - Tolerance for alignment
 */
p.prepareMagneticLines = function (tolerance) {
    var tb = this.getTransformedBounds();
    var globalBounds = this.getGlobalTransformedBounds();

    this.magneticLines = {
        vertical: {},
        horizontal: {},
    };

    // Initialize magnetic rulers (alignment guides)
    // Uncomment and implement as needed
    /*
    var leftLine = new LeftMagneticRuler(tolerance);
    leftLine.x = globalBounds.x;
    leftLine.object = this;

    var rightLine = new RightMagneticRuler(tolerance);
    rightLine.x = globalBounds.x + globalBounds.width;
    rightLine.object = this;

    var centerLine = new CenterMagneticRuler(tolerance);
    centerLine.x = globalBounds.x + globalBounds.width / 2;
    centerLine.object = this;

    var topLine = new TopMagneticRuler(tolerance);
    topLine.y = globalBounds.y;
    topLine.object = this;

    var bottomLine = new BottomMagneticRuler(tolerance);
    bottomLine.y = globalBounds.y + globalBounds.height;
    bottomLine.object = this;

    var centerHorizontalLine = new CenterHorizontalMagneticRuler(tolerance);
    centerHorizontalLine.y = globalBounds.y + globalBounds.height / 2;
    centerHorizontalLine.object = this;

    this.magneticLines.vertical.left = leftLine;
    this.magneticLines.vertical.right = rightLine;
    this.magneticLines.vertical.center = centerLine;
    this.magneticLines.horizontal.top = topLine;
    this.magneticLines.horizontal.bottom = bottomLine;
    this.magneticLines.horizontal.center = centerHorizontalLine;

    Editor.stage.getIRulersLayer().addChild(
      leftLine,
      rightLine,
      centerLine,
      topLine,
      bottomLine,
      centerHorizontalLine
    );
    */
};

/**
 * Get the global transformed bounds of the object
 *
 * @method getGlobalTransformedBounds
 * @return {Object} - The bounds with global coordinates
 */
p.getGlobalTransformedBounds = function () {
    var o = this;
    var mtx = new createjs.Matrix2D();

    do {
        // Prepend each parent's transformation
        mtx.prependTransform(
            o.x,
            o.y,
            o.scaleX,
            o.scaleY,
            o.rotation,
            o.skewX,
            o.skewY,
            o.regX,
            o.regY
        );
    } while ((o = o.parent && o.parent.parent));

    var a = [0, 0, 1];
    var b = [this.width, 0, 1];
    var c = [this.width, this.height, 1];
    var d = [0, this.height, 1];

    // Transform corner points
    var aCords = [a[0] * mtx.a + a[1] * mtx.c + a[2] * mtx.tx, a[0] * mtx.b + a[1] * mtx.d + a[2] * mtx.ty];
    var bCords = [b[0] * mtx.a + b[1] * mtx.c + b[2] * mtx.tx, b[0] * mtx.b + b[1] * mtx.d + b[2] * mtx.ty];
    var cCords = [c[0] * mtx.a + c[1] * mtx.c + c[2] * mtx.tx, c[0] * mtx.b + c[1] * mtx.d + c[2] * mtx.ty];
    var dCords = [d[0] * mtx.a + d[1] * mtx.c + d[2] * mtx.tx, d[0] * mtx.b + d[1] * mtx.d + d[2] * mtx.ty];

    // Determine bounding box
    var startX = Math.min(aCords[0], bCords[0], cCords[0], dCords[0]);
    var startY = Math.min(aCords[1], bCords[1], cCords[1], dCords[1]);

    var boxWidth = Math.max(aCords[0], bCords[0], cCords[0], dCords[0]) - startX;
    var boxHeight = Math.max(aCords[1], bCords[1], cCords[1], dCords[1]) - startY;

    var bounds = {
        x: startX,
        y: startY,
        width: boxWidth,
        height: boxHeight,
    };

    return bounds;
};

/**
 * Get the x-coordinate of the object
 *
 * @method getX
 * @return {Number} - The x-coordinate
 */
p.getX = function () {
    return this.x;
};

/**
 * Check if the object is in an editable area
 *
 * @method isInEditableArea
 * @return {Boolean} - True if in editable area
 */
p.isInEditableArea = function () {
    var parent = this.parent;

    while (parent) {
        if (parent.slope) return true;

        parent = parent.parent;
    }

    return false;
};

export { EditorObject };
