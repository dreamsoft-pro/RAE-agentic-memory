import { useEffect } from 'react';

class KeyboardNavigation extends React.Component<{ anchors: any[] }, { selectedIndex: number }> {
    private goingForward = true;

    constructor(props: { anchors: any[] }) {
        super(props);
        this.state = { selectedIndex: 0 };
    }

    componentDidMount() {
        document.addEventListener('keydown', this.handleKeydown);
    }

    componentWillUnmount() {
        document.removeEventListener('keydown', this.handleKeydown);
    }

    private handleKeydown = (event: KeyboardEvent) => {
        const keyCode = event.keyCode;
        switch (keyCode) {
            case 39: // RIGHT
            case 40: // DOWN
                this.setState(prevState => ({ selectedIndex: Math.min(this.props.anchors.length - 1, prevState.selectedIndex + 1) }));
                break;
            case 38: // UP
            case 37: // LEFT
                this.goingForward = false;
                this.setState(prevState => ({ selectedIndex: Math.max(0, prevState.selectedIndex - 1) }));
                break;
            case 35: // END
                this.setState({ selectedIndex: this.props.anchors.length - 1 });
                break;
            case 36: // HOME
                this.setState({ selectedIndex: 0 });
                break;
            case 32: // SPACE
                event.preventDefault();
                this.activate(this.state.selectedIndex);
                return;
            case 13: // ENTER
                event.preventDefault();
                this.toggleActivation(this.state.selectedIndex);
                return;
        }
    }

    private activate(index: number) {
        console.log(`Activate at index ${index}`);
    }

    private toggleActivation(index: number | false) {
        if (index === false || !this.props.anchors[index]) {
            console.log('Deactivate');
        } else {
            this.activate(index);
        }
    }

    render() {
        return (
            <div>
                {/* Your component rendering logic here */}
            </div>
        );
    }
}

export default KeyboardNavigation;