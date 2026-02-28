import React from "react";

class EditableAreaSettings extends React.Component {

    constructor( props ){

        super (props);

        if( this.props && this.props.editableArea ){

            this.state = {
                rotation: this.props.editableArea.rotation,
                x: this.props.editableArea.x,
                y:  this.props.editableArea.y
            }

        }else {

            this.state = {
                rotation: 0,
                x: 0,
                y: 0
            }

        }

    }

    changeEvent(){

        this.render();

    }

    rotate( e  ){


        if( this.props.editableArea ) {

            this.props.editableArea.setRotation( parseFloat( e.target.value ) );

        }

    }

    setX ( e ) {

        this.props.editableArea.setPosition( parseFloat(e.target.value), this.props.editableArea.y );


    }

    setY ( e ) {

        this.props.editableArea.setPosition( this.props.editableArea.x, parseFloat( e.target.value ) );

    }

    typeOfPrint(e){
        //TODO
    }

    renderPositionTools (){

        var radiobutton1,radiobutton2;

        if( this.props.settings ){

            if ( this.props.settings.vacancy ){

                radiobutton1 = <label>Rozkładówka<input type="radio" name="type_of_print" value="1" checked onChange={this.typeOfPrint.bind(this)}/></label>;
                radiobutton2 = <label>Strona po stronie<input type="radio" name="type_of_print" value="2" onChange={this.typeOfPrint.bind(this)}/></label>;

            }else {

                if( this.props.settings.spread ){

                    radiobutton1 = <label>Rozkładówka<input type="radio" name="type_of_print" value="1" onChange={this.typeOfPrint.bind(this)}/></label>;
                    radiobutton2 = <label>Strona po stronie<input type="radio" name="type_of_print" value="2" checked onChange={this.typeOfPrint.bind(this)}/></label>;

                }else {

                    radiobutton1 = <label>Rozkładówka<input type="radio" name="type_of_print" value="1" checked onChange={this.typeOfPrint.bind(this)}/></label>;
                    radiobutton2 = <label>Strona po stronie<input type="radio" name="type_of_print" value="2" onChange={this.typeOfPrint.bind(this)}/></label>;

                }

            }

            return(

                <div className="position-tools">
                    <div className="section">
                        <h3>Transformacje</h3>
                        <label>Rotacja<input type="number" className="rotate" onChange={this.rotate.bind(this)} value={this.props.settings.rotation}/></label>
                        <label>Pozycja X<input type="number" className="posX" onChange={this.setX.bind(this)} value={this.props.settings.x}/></label>
                        <label>Pozycja Y<input type="number" className="posY" onChange={this.setY.bind(this)} value={this.props.settings.y}/></label>
                    </div>
                    <div className="section">
                        <h3>Ustawienia strony</h3>
                        <label>Sposób druku</label>
                        {radiobutton1}
                        {radiobutton2}
                    </div>
                </div>

            );
        }else {

            return(

                <div className="position-tools">

                </div>

            );

        }

    }

    render (){

        return (
            <div>
                {this.renderPositionTools()}
            </div>
        )

    }

}

class EditorSettings extends React.Component {

	constructor( props ){

        super(props);

        props.jsContext.reactEditorSettings=this
        this.state = {
            theme: null,
            editableArea: null,
            editableAreaSettings: null,
            themePage: null

        }

	}

    setEditableArea ( area ){

        var state = {};
        state.theme = this.state.theme;
        state.themePage = this.state.themePage;
        state.editableArea = area;

        if( area ){

            var eaSettings = {
                rotation : area.rotation,
                x : area.x,
                y : area.y,
                vacancy: area.settings.vacancy
            };

            state.editableAreaSettings = eaSettings;
        }

        this.setState( state );
        this.forceUpdate();

    }

    setThemePage ( themePage ){

        var state = JSON.parse(JSON.stringify(this.state));
        state.themePage = themePage;
        this.setState( state );

    }

    setTheme ( theme ){

        var state = JSON.parse(JSON.stringify(this.state));
        state.theme = theme;
        this.setState( state );

    }

	render(){


		return(

            <div className="editableTool-box-container" ref={this.props.callback}>
                <EditableAreaSettings settings={ this.state.editableAreaSettings } editableArea={this.state.editableArea}/>
            </div>

		);

	}

}

export {EditorSettings};
