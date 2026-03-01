import { useState } from 'react';
import api from '@/lib/api'; // Assuming you have an API client set up as per rule #1

interface SelectableItem {
    element: HTMLElement;
    $element: JQuery<HTMLElement>;
    selected: boolean;
}

const SelectionComponent = () => {
    const [selectedItems, setSelectedItems] = useState<SelectableItem[]>([]);

    const handleSelectChange = async (event: React.MouseEvent) => {
        // Handle the selection logic here
        const targetElement = event.target as HTMLElement;

        if (!targetElement.closest('.selectable-item')) return;

        let itemData = selectedItems.find(item => item.element === targetElement);
        
        if (!itemData) {
            // Create new SelectableItem data structure
            itemData = { element: targetElement, $element: $(targetElement), selected: false };
            setSelectedItems([...selectedItems, itemData]);
        }

        const doSelect = !(event.metaKey || event.ctrlKey) || !$(targetElement).hasClass('ui-selected');

        if (doSelect) {
            // Perform selection
            itemData.selected = true;
            $(targetElement).addClass('ui-selecting');
            
            try {
                // Example API call for selected items
                await api.selectItem(itemData.element);
            } catch (error) {
                console.error("Failed to select item:", error);
            }
        } else {
            // Perform unselection
            itemData.selected = false;
            $(targetElement).addClass('ui-unselecting');
            
            try {
                // Example API call for deselected items
                await api.unSelectItem(itemData.element);
            } catch (error) {
                console.error("Failed to unselect item:", error);
            }
        }

        setSelectedItems([...selectedItems.map(item => ({
            ...item,
            selected: doSelect ? true : false
        })].filter(item => item.selected === undefined));
    };

    return (
        <div className="selection-container" onClick={handleSelectChange}>
            {/* Your selectable items go here */}
        </div>
    );
};

export default SelectionComponent;