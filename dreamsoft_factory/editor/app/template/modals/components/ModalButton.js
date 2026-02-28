import React from 'react'

const ModalButton = ({text, ...props}) => {
    return (
        <button
            type={"button"}
            data-bs-dismiss="modal"
            aria-label={text}
            {...props}
        >
            {text}
        </button>
    )
}

export default ModalButton