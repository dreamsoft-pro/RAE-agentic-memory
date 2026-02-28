import React, {useEffect, useRef} from 'react'

const Slider = ({className = "", handleOnChange, handleOnStop = () => {}, ...props}) => {
    const sliderRef = useRef(null);

    const handleMouseLeave = () => {
        handleOnStop();
    };

    useEffect(() => {
        const slider = sliderRef.current;

        const handleScroll = (e) => {
            e.stopPropagation();
            e.preventDefault();

            const { step, max, min, value } = sliderRef.current;
            const stepMultiplier = max - min / (1 / step);

            const sliderProps = {
                step: parseFloat(step),
                max: parseFloat(max),
                min: parseFloat(min),
                value: parseFloat(value)
            };

            let toFixedValue = (1 / sliderProps.step).toString().length - 1;

            if (e.deltaY < 0 && sliderProps.value + sliderProps.step <= sliderProps.max) {
                handleOnChange(
                    parseFloat(parseFloat((Math.round(sliderProps.value * (1 / sliderProps.step)) / (1 / sliderProps.step) + sliderProps.step * stepMultiplier)).toFixed(toFixedValue))
                );

            } else if (e.deltaY > 0 && sliderProps.value - sliderProps.step >= sliderProps.min) {
                handleOnChange(
                    parseFloat(parseFloat((Math.round(sliderProps.value * (1 / sliderProps.step)) / (1 / sliderProps.step) - sliderProps.step * stepMultiplier)).toFixed(toFixedValue))
                );
            }
        };

        slider.addEventListener("wheel", (e) => handleScroll(e));
        slider.addEventListener("mouseleave", () => handleMouseLeave());

        return () => {
            slider.removeEventListener("wheel", handleScroll);
            slider.removeEventListener("mouseleave", () => handleMouseLeave());
        };

    }, []);

    return (
        <input
            ref={sliderRef}
            type={"range"}
            className={`zoom-slider ${className}`}
            onChange={(e) => handleOnChange(parseFloat(e.target.value))}
            {...props}
        />
    )
}

export default Slider