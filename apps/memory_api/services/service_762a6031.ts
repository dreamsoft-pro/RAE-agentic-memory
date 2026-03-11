import React, { useEffect } from 'react';
import api from '@/lib/api'; // As per the rule

interface TabProps {
  className: string;
}

const TabItem: React.FC<TabProps> = ({ className }) => {
  const [isDisabled, setIsDisabled] = React.useState<boolean>(false);

  useEffect(() => {
    document.querySelectorAll(`.${className} > li`).forEach((li) => {
      li.addEventListener('mousedown', (event: MouseEvent) => {
        if (li.classList.contains('ui-state-disabled')) {
          event.preventDefault();
        }
      });

      // support: IE <9
      li.querySelectorAll('.ui-tabs-anchor').forEach((anchor) => {
        anchor.addEventListener('focus', () => {
          const parentLi = anchor.closest('li');
          if (parentLi?.classList.contains('ui-state-disabled')) {
            anchor.blur();
          }
        });
      });

    });
  }, [className]);

  return null; // Render nothing since this is for event handling only
};

export default TabItem;