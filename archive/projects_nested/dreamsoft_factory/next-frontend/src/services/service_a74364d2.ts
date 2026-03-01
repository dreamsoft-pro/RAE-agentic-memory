import api from '@/lib/api';
import { useEffect } from 'react';

interface Props {
  mode: string;
  duration?: number;
  easing?: string;
}

class SizeEffect extends React.Component<Props, {}> {

  constructor(props: Props) {
    super(props);
    this.state = {};
  }

  async componentDidMount() {
    try {
      const response = await api.get('/some-resource');
      
      // Assuming response contains properties that dictate the effect
      const o = { color: '#ffff99', duration: this.props.duration || 500, easing: this.props.easing || 'linear' };
      if (this.props.mode === "hide") {
        this.hide();
      } else {
        await this.applyEffect(o);
      }
    } catch (error) {
      console.error("Failed to fetch data for effect:", error);
    }
  }

  async applyEffect(o: { color?: string, duration?: number, easing?: string }) {
    const element = document.getElementById('effect-element'); // Replace with your selector
    if (!element) return;

    // Apply initial style changes (if needed)
    element.style.backgroundColor = o.color || "#ffff99";
    
    // Animate the effect here. This is a placeholder for actual animation logic.
    await new Promise(resolve => setTimeout(() => resolve(), o.duration || 500));
    
    if (this.props.mode === "hide") {
      this.hide();
    }
  }

  hide() {
    const element = document.getElementById('effect-element'); // Replace with your selector
    if (!element) return;
    element.style.display = 'none';
  }

  render() {
    return (
      <div id="effect-element" style={{ width: "100px", height: "100px", backgroundColor: "#ffff99" }}>
        {/* Your component content here */}
      </div>
    );
  }
}

export default SizeEffect;