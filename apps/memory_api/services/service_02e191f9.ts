import React, { Component } from 'react';
import axios from '@/lib/api'; // Assuming this is an Axios wrapper.

// Mock data for simplicity - replace with actual logic
const MenuItem = ({ index }) => <div id={`menu-item-${index}`} className="menuItem">Item {index}</div>;

interface MenuProps {
  items: Array<{ index: number }>;
}

interface MenuState {
  focusIndex?: number;
  isOpen: boolean;
}

class SelectMenu extends Component<MenuProps, MenuState> {

  constructor(props: MenuProps) {
    super(props);
    this.state = {
      isOpen: false,
      focusIndex: undefined
    };
  }

  componentDidMount() {
    // Adjust menu styles to dropdown on mount or other event.
    this.adjustMenuStyles();
  }

  adjustMenuStyles = () => {
    const menuItems = document.querySelectorAll('.menuItem');
    
    // Class manipulation using inline style, className, etc. should be done differently in React.
    Array.from(menuItems).forEach((item, index) => {
      item.classList.add("ui-corner-bottom");
      item.classList.remove("ui-corner-all");
      
      // Simulating the aria-activedescendant update
      if (index === this.state.focusIndex) {
        document.getElementById('select-button').setAttribute(
          'aria-activedescendant',
          `menu-item-${index}`
        );
      }
    });
  }

  handleFocus = (event: React.FocusEvent<HTMLInputElement>, index?: number) => {
    event.preventDefault(); // Prevent default browser focus handling

    if (this.state.focusIndex !== index) { // Check for new item focused
      this.setState({ focusIndex: index }, () => {
        console.log('Focused on:', index);  // Custom trigger logic
        
        if (!this.state.isOpen) {
          axios.get(`some-endpoint/${index}`) // Mock API call to simulate select action.
            .then(response => console.log(response))
            .catch(error => console.error(error));
        }
      });
    }
  }

  render() {
    const { items } = this.props;
    
    return (
      <div>
        <button id="select-button" onFocus={(event) => this.handleFocus(event, undefined)}>Select</button>
        
        {/* Menu items rendered as list */}
        <ul className="menu">
          {items.map((item, index) => (
            <MenuItem key={index} index={item.index} />
          ))}
        </ul>
      </div>
    );
  }
}

export default SelectMenu;