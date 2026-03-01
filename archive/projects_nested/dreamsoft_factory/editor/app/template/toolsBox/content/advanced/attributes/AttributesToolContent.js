import React from 'react';
import ProductAttributes from '../../../../ProductAttributes';

const AttributesToolContent = ({editor, className = ""}) => {
    editor.template.productAttributes = <ProductAttributes editor={editor} selectedAttributes={editor.complexProduct[2]}/>;

    return (
        <div id="attributes-content" className={`${className}`}>
            {/*<div id="attributesSelector"></div>*/}
            {/*<div id="attributesOptionGeneration">*/}
            {/*    Dostosuj wygląd edytora względem cech:*/}
            {/*</div>*/}
            {/*/!* Space for product attributes *!/*/}
            {/*<div id="product-attributes"></div>*/}
            {/*/!* Base view layer *!/*/}
            {/*<div id="baseViewLayer"></div>*/}
            {editor.template.productAttributes}
        </div>

    );
}

export default AttributesToolContent;
