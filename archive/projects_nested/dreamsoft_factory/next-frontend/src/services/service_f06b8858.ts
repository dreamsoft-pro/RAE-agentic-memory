import api from '@/lib/api';
import { useEffect } from 'react';

type Props = {
    mode?: string;
    duration: number;
    easing: string;
    done: () => void;
};

const HighlightEffect: React.FC<Props> = ({ mode, duration, easing, done }) => {

    const applyHighlight = async (elementRef: HTMLDivElement | null) => {
        if (!elementRef) return;

        const elem = elementRef;
        const propsToSave = ["backgroundImage", "backgroundColor", "opacity"];
        const initialBackgroundColor = elem.style.backgroundColor || 'transparent';

        // Save original properties before making changes
        const savedProps = Object.entries(propsToSave.reduce((acc, prop) => {
            acc[prop] = window.getComputedStyle(elem).getPropertyValue(prop);
            return acc;
        }, {} as {[key: string]: string}));

        try {
            let animation: { [key: string]: any } = { backgroundColor: initialBackgroundColor };
            
            if (mode === 'hide') {
                animation.opacity = 0;
            }

            await animateProperties(elem, animation, duration, easing);

            // Cleanup after animation
            elem.style.backgroundColor = savedProps['backgroundColor'];
            if (mode === 'hide' && !animation.opacity) {
                elem.style.display = 'none';
            }
        } catch (error) {
            console.error('Error during highlight effect:', error);
        } finally {
            done();
        }

    };

    const animateProperties = async (elem: HTMLElement, animations: { [key: string]: any }, duration: number, easing: string) => {
        await new Promise<void>(resolve => {
            elem.animate(animations, {
                duration,
                easing
            }).onfinish = () => resolve();
        });
    };

    useEffect(() => {
        const performHighlightEffect = async () => {
            applyHighlight(document.getElementById('elementId'));
        };
        
        performHighlightEffect();

    }, [mode, duration, easing]);

    return null; // Return null as this component is purely for side-effect operations
};

export default HighlightEffect;