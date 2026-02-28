import React, {useEffect, useRef, useState} from 'react'

const DropdownOnHover = ({elements, children}) => {
    const dropdownRef = useRef(null)
    const hoverElementRef = useRef(null)
    const dropdownContainerRef = useRef(null)

    const [show, setShow] = useState(false)
    let wasOnButton = false

    useEffect(() => {
        const handleHoverOutside = (e) => {
            if (hoverElementRef.current && hoverElementRef.current.contains(e.target)) {
                setShow(true)
                wasOnButton = true
            } else if (wasOnButton && dropdownRef.current.contains(e.target)) {
                setShow(true)
            } else {
                wasOnButton = false;
                setShow(false)
            }
        }

        document.addEventListener('mouseover', (e) => handleHoverOutside(e))

        return () => {
            document.removeEventListener('mouseover', handleHoverOutside)
        }
    }, []);

    return (
        <div
            className={'dropdown-on-hover-container'}
            ref={dropdownContainerRef}
        >
            <div ref={hoverElementRef}>
                {children}
            </div>
            <div ref={dropdownRef} className={`dropdown-content ${show ? "visible" : ""}`}>
                {elements.map((item, index) => (
                    <DropdownItem key={index} {...item}>
                        <React.Fragment>
                            {item.element}
                        </React.Fragment>
                    </DropdownItem>
                ))}
            </div>
        </div>
    )
}

const DropdownItem = ({title, description, children, ...props}) => {
    return (
        <div
            className={'dropdown-item'}
            {...props}
        >
            {children}
            <div className={'item-text-container'}>
                <p className={'item-title'}>{title}</p>
                <span className={'item-description'}>{description}</span>
            </div>
        </div>
    )
}

export default DropdownOnHover