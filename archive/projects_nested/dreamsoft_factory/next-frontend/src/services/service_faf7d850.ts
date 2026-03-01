import api from '@/lib/api';

class MyClass {
    async performTransferOperation(): Promise<void> {
        try {
            const elem = document.querySelector('#myElement')!; // Replace with actual query if necessary.
            const target = document.querySelector('#targetElement')!;
            
            const targetFixed = window.getComputedStyle(target).position === 'fixed';
            let body: HTMLElement;
            if (document.body) {
                body = document.body;
            } else {
                throw new Error('Document body is not available.');
            }
            
            const fixTop = targetFixed ? body.scrollTop : 0;
            const fixLeft = targetFixed ? body.scrollLeft : 0;

            const endPosition = target.getBoundingClientRect();
            const animation: { [key: string]: number } = {
                top: endPosition.top - fixTop,
                left: endPosition.left - fixLeft,
                height: target.offsetHeight,
                width: target.offsetWidth
            };

            const startPosition = elem.getBoundingClientRect();

            const transferDiv = document.createElement('div');
            transferDiv.className = 'ui-effects-transfer';
            
            if (document.body) {
                document.body.appendChild(transferDiv);
            } else {
                throw new Error('Document body is not available.');
            }

            Object.assign(transferDiv.style, {
                position: targetFixed ? "fixed" : "absolute",
                top: `${startPosition.top - fixTop}px`,
                left: `${startPosition.left - fixLeft}px`,
                height: `${elem.offsetHeight}px`,
                width: `${elem.offsetWidth}px`
            });

            await new Promise((resolve) => setTimeout(resolve, 10)); // Simulate async operation
            transferDiv.animate(animation, {
                duration: 2000,
                easing: 'linear',
                fill: 'forwards',
                complete: () => {
                    document.body.removeChild(transferDiv);
                    console.log('Transfer animation completed.');
                }
            });
        } catch (error) {
            console.error("Error performing transfer operation:", error);
        }
    }

    async fetchData() {
        try {
            const response = await api.get('/api/some-endpoint');
            console.log(response.data);
            this.performTransferOperation();
        } catch (error) {
            console.error('Failed to fetch data:', error);
        }
    }
}

export default MyClass;