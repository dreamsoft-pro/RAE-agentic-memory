import React, { useEffect, useState } from 'react';

interface ScopeProps {
    opened: boolean;
    hideOverflow: boolean;
    nextImage: () => void;
    prevImage: () => void;
    closeGallery: () => void;
}

const GalleryComponent: React.FC<ScopeProps> = (props) => {
    const [opened, setOpened] = useState(props.opened);

    useEffect(() => {
        function handleKeyDown(event: KeyboardEvent): void {
            if (!opened) return;

            let which = event.which;
            if (which === keys_codes.esc) {
                props.closeGallery();
            } else if (which === keys_codes.right || which === keys_codes.enter) {
                props.nextImage();
            } else if (which === keys_codes.left) {
                props.prevImage();
            }
        }

        document.body.addEventListener('keydown', handleKeyDown);
        return () => {
            document.body.removeEventListener('keydown', handleKeyDown);
        };
    }, [opened, props.closeGallery, props.nextImage, props.prevImage]);

    const closeGallery = (): void => {
        setOpened(false);
        if (props.hideOverflow) {
            document.body.style.overflow = '';
        }
    };

    return null; // Since this component is mainly for handling events and state, it returns nothing.
};

export default GalleryComponent;