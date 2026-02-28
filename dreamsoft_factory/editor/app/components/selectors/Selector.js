import React, {useEffect, useRef, useState} from 'react'

const Selector = ({elements, onChange, renderItem, selected = 0, gray = false, ...props}) => {
    const [isExpanded, setIsExpanded] = useState(false)
    const [selectedItem, setSelectedItem] = useState(elements[selected])

    const dropdown = useRef(null)
    const dropdownContent = useRef(null)

    const shrink = () => {
        setIsExpanded(false)
        $(dropdownContent.current)
        .animate({
            maxHeight: 0,
        }, 300)
        .animate({
            opacity: 0
        }, 300, () => {
            $(dropdownContent.current).hide();
        });
    }

    const expand = () => {
        setIsExpanded(true)
        $(dropdownContent.current)
        .show()
        .animate({
            maxHeight: "11rem",
        }, 300)
        .animate({
            opacity: 1
        }, 300);
    }

    const handleClick = () => {
        if (!isExpanded) {
            expand()
        } else {
            shrink()
        }
    }

    const handleOnChange = (item) => {
        onChange(item);
        setSelectedItem(item)
        shrink()
    }

    useEffect(() => {
        setSelectedItem(elements[selected])
    }, [selected])

    useEffect(() => {
        if (!isExpanded) {
            shrink()
        }

        const handleClickOutside = (e) => {
            if (dropdownContent.current && !dropdownContent.current.contains(e.target) && !dropdown.current.contains(e.target)) {
                shrink()
            }
        }

        document.addEventListener('mousedown', handleClickOutside)

        return () => {
            document.removeEventListener('mousedown', handleClickOutside)
        }
    }, [])

    return (
        <div
            ref={dropdown}
            className={'dropdown-container'}
            {...props}
        >
            <Item
                className={gray ? "gray" : ""}
                selected
                isExpanded={isExpanded}
                onClick={handleClick}
            >
                <span className={'item-name'}>
                    {selectedItem.value || ""}
                </span>
            </Item>
            <div className={'dropdown'}>
                <div
                    ref={dropdownContent}
                    className={'dropdown-content'}
                >
                    {elements.map((item, index) => (
                        <Item
                            key={index}
                            onClick={() => handleOnChange(item)}
                        >
                            {renderItem(item)}
                        </Item>
                    ))}
                </div>
            </div>
        </div>
    )
}

const Item = ({isExpanded, children, className = "", selected = false, ...props}) => {
    return (
        <div
            className={`dropdown-item ${className} ${selected ? `selected ${isExpanded ? "open" : ""}` : ""}`}
            {...props}

        >
            {children}
        </div>
    )
}

export default Selector