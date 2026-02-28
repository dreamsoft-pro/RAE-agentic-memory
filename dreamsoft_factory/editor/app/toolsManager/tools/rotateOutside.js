var EditComponent = require('./../../EditComponent').EditComponent;

var size = 32;

const rotatorContainer = new createjs.Container()

const rotatorImage = new Image()
rotatorImage.src = `${EDITOR_ENV.templatesDir}/images/from-figma/refresh.svg`;

rotatorImage.onload = () => {
	const rotatorBitmap = new createjs.Bitmap(rotatorImage);
	// rotatorBitmap.scaleX = rotatorBitmap.scaleY;
	rotatorBitmap.regX = rotatorImage.width / 2;
	rotatorBitmap.regY = rotatorImage.height / 2;

	rotatorContainer.addChild(rotatorBitmap)
}

var rotator = new createjs.Shape();

rotator.graphics
	.beginFill("#565656")
	.drawCircle(0,0, size / 2)
	.ss(2)
	.s("#a8a8a8")
	.arc(0,0, size/2+1,0, Math.PI*2);

rotatorContainer.addChild(rotator);

var rotateComponent = [

	{
		event : 'mousedown',
		'function' : function(e){

			e.stopPropagation();
			var editing_id = this.id;
			var editingObject = this.objectReference;

			editingObject.history_tmp['action'] = 'rotation';
			editingObject.history_tmp['info'] = {};
			editingObject.history_tmp['info']['before'] = editingObject.rotation;
			editingObject.history_tmp['info']['id'] = editingObject.id;

		}
	},

	{
		event: 'pressmove',
		'function' : function(e){
			e.stopPropagation();
			var editing_id = this.id;
			var editingObject = this.objectReference;
			var component = e.currentTarget;
			var parent = e.target.parent;	
		
			var localCursorPosition = component.parent.globalToLocal( e.stageX, e.stageY);
			var vector1 =  [0, (editingObject.trueHeight/2 + 40)];
			var vector2 =  [localCursorPosition.x * editingObject.scaleX - editingObject.width/2  * editingObject.scaleX, -localCursorPosition.y* editingObject.scaleY + (editingObject.height/2)  * editingObject.scaleY];
			//console.log( [localCursorPosition.x - 150, -localCursorPosition.y + 150] );
			var kat = ( ((vector1[0]*vector2[0]+ vector1[1]*vector2[1])/(Math.sqrt(vector1[0]*vector1[0] + vector1[1]*vector1[1])*Math.sqrt(vector2[0]*vector2[0]+vector2[1]*vector2[1]))));
			
			if( vector2[0] < 0){
				editingObject.rotate( -(180/Math.PI)*Math.acos(kat) + (( editingObject.scaleY < 0) ?  180  : 0));

			}
			else {
				editingObject.rotate( (180/Math.PI)*Math.acos(kat) + (( editingObject.scaleY < 0) ?  180  : 0));

			}
			
			if( editingObject.mask ){
				
				editingObject.mask.x = editingObject.x;
				editingObject.mask.y = editingObject.y;
				editingObject.mask.regX = editingObject.regX;
				editingObject.mask.regY = editingObject.regY;

			}

            //Editor.webSocketControllers.productType.adminProject.view.editorObject.rotate( editingObject.rotation, editingObject.dbID );
            
			
			this.tools.init();
		}
	},


	{
		event : 'pressup',
		'function' : function(e){
			e.stopPropagation();
			var editing_id = this.id;
			var editingObject = this.objectReference;
			editingObject.dispatchEvent('rotate');
			editingObject.history_tmp['info']['after'] = editingObject.rotation;

			/*
			if( editingObject.history_tmp['info'].before != editingObject.history_tmp['info'].after )
				Editor.addToHistory( $.extend(true, {},editingObject.getHistoryElem()) );

			if( ! editingObject.isInEditableArea() ){

				editingObject.updateTransformInDB();

			}
			*/

		}
	}
];

export var rotateOutside = new EditComponent('right-bottom-scale', 'click', rotatorContainer, 'aslb', rotateComponent);
