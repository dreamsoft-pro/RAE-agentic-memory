import api from '@/lib/api';
import { useEffect, useRef } from 'react';

type ScaleEffectProps = {
    el: HTMLElement | null;
};

const EffectScaleComponent: React.FC<ScaleEffectProps> = ({ el }) => {
    const doneRef = useRef<(status?: boolean) => void>(() => {});

    useEffect(() => {
        if (!el) return;

        // Define positioning logic
        const positionEl = async () => {
            if (position === 'static') {
                el.style.position = 'relative';
                el.style.top = `${el.to.top}px`;
                el.style.left = `${el.to.left}px`;
            } else {
                await Promise.all(['top', 'left'].map(async pos => {
                    const str = el.style.getPropertyValue(pos);
                    let val: number | undefined;
                    if (str !== 'auto') {
                        val = parseInt(str, 10);
                    }

                    el.style.setProperty(
                        pos,
                        val === undefined ? `${el.to[pos as keyof typeof el.to]}px` : `${val + el.to[pos as keyof typeof el.to]}px`
                    );
                }));
            }
        };

        // Placeholder for the original done function
        const done = (status?: boolean) => {
            console.log('Effect completed', status);
            doneRef.current(status);
        };

        positionEl().then(done);

        return () => {
            doneRef.current();
        };
    }, [el]);

    return null;
};

export default EffectScaleComponent;