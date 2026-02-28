import React, {useEffect, useRef} from 'react'

const Switch = ({
    id,
    value,
    label = {close: "", open: ""},
    onChange = () => {},
    defaultOn = false,
    ...props
}) => {
    const switchRef = useRef(null)

    useEffect(() => {
        if (defaultOn) {
            switchRef.current.checked = true;
        }
    }, []);


    return (
        <div className={'switch-container'}>
            <span>
                {label.close}
            </span>
            <div className={"switch toggle-switch"}>
                <input
                    ref={switchRef}
                    className={"switch toggle-input"}
                    id={id}
                    type={"checkbox"}
                    {...props}
                />
                <label
                    onClick={() => onChange()}
                    className={"switch toggle-label"}
                    htmlFor={id}>
                </label>
            </div>
            <span>
                {label.open}
            </span>
        </div>
    )

}

export default Switch