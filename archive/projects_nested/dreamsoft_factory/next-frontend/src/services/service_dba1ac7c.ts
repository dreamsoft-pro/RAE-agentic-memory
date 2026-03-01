import React, { useEffect } from 'react';
import api from '@/lib/api'; // Assuming this is a custom API module

interface Props {
    origin?: any;
    original: any; // Adjust according to actual types
    el: HTMLElement;
    resource: string | null;
    url: string | null;
}

const EffectComponent = (props: Props) => {
    const { origin, original, el, resource, url } = props;

    useEffect(() => {
        if (!origin || !original || !el) return; // Ensure all variables are defined before use

        const animate = async () => {
            let baseline;
            try {
                baseline = await getBaseline(origin, original);
            } catch (error) {
                console.error('Failed to calculate baseline:', error);
                return;
            }

            el.style.top = `${(original.outerHeight - el.offsetHeight) * baseline.y}px`;
            el.style.left = `${(original.outerWidth - el.offsetWidth) * baseline.x}px`;

            if (resource !== null && url !== null) {
                // Assuming scale is a prop or state
                const { scale } = props;

                if (scale === 'content' || scale === 'both') {
                    // Code for adding margins/font-size etc.
                    let vProps: string[] = ["marginTop", "marginBottom"];
                    let hProps: string[] = ["marginLeft", "marginRight"];
                    let cProps: string[] = [];

                    el.style.marginTop = original.marginTop;
                    el.style.marginBottom = original.marginBottom;
                    // Add other props as needed

                    vProps = [...vProps, ...cProps];
                    hProps = [...hProps];

                    const allProps = [...vProps, ...hProps];

                    // Logic to animate these properties
                }
            }
        };

        animate();
    }, [origin, original, el, resource, url]);

    return null; // Since this is a side-effect component that performs animations
};

// Helper function for getBaseline
const getBaseline = async (origin: any, original: any) => {
    // Assume this fetches the baseline data from an API or calculates it
    const response = await api.getBaseline(origin, original);
    return response.data;
};

export default EffectComponent;