/**
 * Service: SliderCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import * as React from 'react';
import { useState, useEffect } from 'react';
import { observer } from 'mobx-react';
import _ from 'lodash';
import SettingService from './SettingService'; // Adjust the import according to your project structure

interface SliderData {
    files: Array<{ fileID: number, url: string, link: string }>;
}

const SliderCtrl: React.FC = () => {
    const [slides, setSlides] = useState<Array<{ name: string, url: string, link: string }>>([]);
    const [sliderOptions, setSliderOptions] = useState({ sliderAutoSlide: 3, sliderTransition: 'slide' });
    const [sliderText, setSliderText] = useState('');
    const [sliderHeight, setSliderHeight] = useState({ height: '210px' });

    useEffect(() => {
        const handleSliderData = (data: any) => {
            if (!_.isEmpty(data)) {
                const settingService = new SettingService('bannerSlider');
                settingService.getPublicSettings().then((settingsData: any) => {
                    if (settingsData.sliderAutoSlide) {
                        setSliderOptions({ ...sliderOptions, sliderAutoSlide: settingsData.sliderAutoSlide.value });
                    }
                    if (settingsData.sliderTransition) {
                        setSliderOptions({ ...sliderOptions, sliderTransition: settingsData.sliderTransition.value });
                    }

                    const tmpSlides = data.map((oneSlider: SliderData) => 
                        oneSlider.files.map((oneFile: { fileID: number, url: string, link: string }) => ({ name: `Image${oneFile.fileID}`, url: oneFile.url, link: oneFile.link }))
                    );

                    setSlides(tmpSlides);
                });
            } else {
                setSlides([]);
            }
        };

        const handleSliderEvent = (event: any, data: any) => {
            if (event && event.type === 'Slider:data') {
                handleSliderData(data);
            }
        };

        // Assuming $rootScope is a global state management or context provider in your Angular app
        // You might need to adjust this part according to how you manage events in your React/MobX setup
        // For example, if using Redux, it would be dispatch(action) and subscribe in the component
        window.addEventListener('Slider:data', handleSliderEvent);

        return () => {
            window.removeEventListener('Slider:data', handleSliderEvent);
        };
    }, []);

    useEffect(() => {
        setSliderText(`rn-carousel rn-carousel-index="sliderIndex" rn-carousel-controls rn-carousel-auto-slide="${sliderOptions.sliderAutoSlide}"` +
            ' rn-carousel-pause-on-hover rn-carousel-buffered rn-carousel-transition="' + sliderOptions.sliderTransition + '" rn-carousel-controls-allow-loop');
    }, [sliderOptions]);

    return (
        <div style={sliderHeight}>
            {/* Render your carousel or slider component here using the slides and options */}
            {slides.map((slide, index) => (
                <img key={index} src={slide.url} alt={slide.name} />
            ))}
        </div>
    );
};

export default observer(SliderCtrl);