import React, { useEffect, useState} from 'react';
import Selector from "../components/selectors/Selector";

const ProductAttributes = ({selectedAttributes, editor}) => {
    const [selected, setSelected] = useState(selectedAttributes);

    const changeItem = (item) => {
        setSelected(prev => {
            const newSelected = {
                ...prev,
                [item.attributeIndex]: {
                    ...prev[item.attributeIndex],
                    [item.attributeId]: item.data
                }
            }
            editor.selectedProductAttributes = newSelected;
            editor.services.calculatePrice()

            return newSelected
        });
    }

    useEffect(() => {
        editor.selectedProductAttributes = selectedAttributes;
    }, []);

    return (
        <>
            {editor.complexProduct[0].map((elem, index) => selectsForProduct(elem, index, editor, selected, changeItem))}
        </>
    );
}

const selectsForProduct = (productType, index, editor, selected, changeItem) => {
    let product = editor.productData[index].products.find((p) => p.typeID === productType);
    if (!product) {
        return <div key={index}></div>;
    }

    const format = editor.complexProduct[1][index];
    const attributes = product.formats[`${format}`]?.attributes;
    const selects = [];

    if (attributes) {
        let excludes = [];

        Object.keys(attributes).forEach((key) => {
            const options = [];
            const attrOptions = attributes[key].options;

            Object.keys(attrOptions).forEach((optKey) => {
                if (optKey === selected[index][key]) {
                    excludes = excludes.concat(attrOptions[optKey].excludes);
                }

                if (!excludes.includes(parseInt(optKey))) {
                    options.push(
                        {
                            data: optKey,
                            // value as item name
                            value: attrOptions[optKey].name,
                            attributeIndex: index,
                            attributeId: key
                        }
                    );
                }
            });

            const renderItem = (item) => {
                return (
                    <span className={'item-name'}>
                        {item.value}
                    </span>
                )
            }

            selects.push(
                <Selector
                    renderItem={renderItem}
                    key={key}
                    selected={0}
                    elements={options}
                    onChange={changeItem}
                />
            );
        });
    }

    return (
        <div className="product-attributes" key={index}>
            <div className="main-tool-button">{product.typeName}</div>
            {selects}
        </div>
    );
};

export default ProductAttributes