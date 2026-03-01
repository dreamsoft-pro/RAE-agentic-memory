/**
 * Service: category
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useState, useEffect } from 'react';
import { Accordion, AccordionGroup } from './AccordionComponents'; // Assuming you have similar components or adapt them accordingly
import { GalleryComponent } from './GalleryComponent'; // Adjust the import based on your file structure

const Category: React.FC = () => {
    const [descriptions, setDescriptions] = useState([]);
    const [galleries, setGalleries] = useState([]);
    const [currentLang, setCurrentLang] = useState({ code: '' });

    useEffect(() => {
        // Fetch data logic here or update state based on dependencies
    }, [descriptions, galleries, currentLang]);

    return (
        <div>
            <div ng-if="attributeDescView == 3">
                <div className="row">
                    <div className="col-xs-12 col-sm-12 col-md-12 col-lg-12">
                        <Accordion>
                            {descriptions.map((description, index) => (
                                <AccordionGroup key={index} isOpen={description.isOpen} ngClass={{ 'panel-accordion': true, 'active': description.isOpen }}>
                                    <AccordionHeading>
                                        {description.langs[currentLang.code].name}
                                        <i className="pull-right fa" ngClass={{ 'fa-chevron-down': description.isOpen, 'fa-chevron-right': !description.isOpen }}></i>
                                    </AccordionHeading>
                                    <div dangerouslySetInnerHTML={{ __html: description.langs[currentLang.code].description }} />
                                </AccordionGroup>
                            ))}
                        </Accordion>
                        {galleries.length > 0 && (
                            <div className="row" id="row-category-gallery">
                                {galleries.map((gallery, index) => (
                                    gallery.items.length > 0 && (
                                        <div key={index} className="col-xs-12">
                                            <h3>{gallery.langs[currentLang.code].name}</h3>
                                            <GalleryComponent images={gallery.items} thumbsNum={gallery.items.length} />
                                        </div>
                                    )
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Category;