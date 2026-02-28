import React from 'react';
import axios from '@/lib/api'; // Assuming this is your custom Axios wrapper

class MenuWidget extends React.Component {
  private menu: any; // Replace `any` with appropriate type if available

  getMenu = () => {
    return this.menu;
  };

  _renderMenu = (ul: HTMLElement, items: Array<any>) => { // Replace `any` with appropriate item type
    let currentOptgroup = "";

    for (let index in items) {
      const item = items[index];
      
      if (item.optgroup !== currentOptgroup) {
        $(`<li class="ui-selectmenu-optgroup ui-menu-divider${item.element.parent('optgroup').prop('disabled') ? ' ui-state-disabled' : ''}">`).text(item.optgroup).appendTo(ul);

        currentOptgroup = item.optgroup;
      }

      this._renderItemData(ul, item);
    }
  };

  _renderItemData = (ul: HTMLElement, item: any) => { // Replace `any` with appropriate type
    return this._renderItem(ul, item).data('ui-selectmenu-item', item);
  };

  _renderItem = (ul: HTMLElement, item: any) => { // Replace `any` with appropriate type
    const li = $('<li>');

    if (item.disabled) {
      li.addClass('ui-state-disabled');
    }
    this._setText(li, item.label);

    return li.appendTo(ul);
  };

  _setText = (element: HTMLElement, value: string | boolean) => {
    element.text(value ? value : '&#160;');
  };
}

export default MenuWidget;