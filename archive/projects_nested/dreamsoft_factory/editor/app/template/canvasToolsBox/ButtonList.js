import React from 'react';
import SwapTemplate from './buttons/SwapTemplate';
import AddText from './buttons/AddText';
import RemoveText from './buttons/RemoveText';
import AddImage from './buttons/AddImage';
import RemoveImage from './buttons/RemoveImage';

export const ButtonList = [
    {
      id: 'swapTemplate',
      Component: SwapTemplate,
      helperText: 'Zmień układ szablonu projektu',
      showAlways: true
    },
    {
      id: 'addText',
      Component: AddText,
      helperText: 'Dodaj nowy tekst do projektu',
      showAlways: true
    },
    {
      id: 'removeText',
      Component: RemoveText,
      helperText: 'Usuń dodany tekst',
      showAlways: false
    },
    {
      id: 'addImage',
      Component: AddImage,
      helperText: 'Dodaj nowe zdjęcie do projektu',
      showAlways: true
    },
    {
      id: 'removeImage',
      Component: RemoveImage,
      helperText: 'Usuń dodane zdjęcie',
      showAlways: false
    }
  ];