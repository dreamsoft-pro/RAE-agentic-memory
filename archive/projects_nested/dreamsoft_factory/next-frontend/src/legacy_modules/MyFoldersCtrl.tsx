/**
 * Service: MyFoldersCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useScope } from './path-to-scope-hook'; // Adjust this import according to your project structure
import { useModal } from './path-to-modal-hook'; // Import modal hook if used
import { useEffect } from 'react';

const MyFoldersCtrl: React.FC = () => {
  const ctx = useScope(); // Assuming you have a custom hook for scope access
  const [map, setMap] = React.useState<google.maps.Map | null>(null);
  const [folder, setFolder] = React.useState<any>(null);
  const [position, setPosition] = React.useState<google.maps.LatLngLiteral | null>(null);

  useEffect(() => {
    if (folder) {
      const initMap = () => {
        // Initialize map logic here
        const mapOptions: google.maps.MapOptions = {
          center: { lat: parseFloat(folder.location.lat), lng: parseFloat(folder.location.lng) },
          zoom: 8,
        };
        const newMap = new google.maps.Map(document.createElement('div'), mapOptions);
        setMap(newMap);
      };
      initMap();
    }
  }, [folder]);

  useEffect(() => {
    if (map && folder) {
      const marker = new google.maps.Marker({
        position: { lat: parseFloat(folder.location.lat), lng: parseFloat(folder.location.lng) },
        map,
        icon: {
          url: folder.imageFiles[0].thumbnail,
          scaledSize: new google.maps.Size(40, 40), // Adjust width and height as needed
        },
      });

      marker.folderData = folder;

      marker.addListener('click', function (e) {
        const click = () => {
          // Navigate to the photo zone logic here
          console.log(`Folder ID: ${marker.folderData._id}`);
        };

        const elem = document.createElement('div');
        elem.className = 'folderDataInfo';

        const titleElem = document.createElement('h3');
        titleElem.innerHTML = marker.folderData.folderName;

        const link = document.createElement('a');
        link.className = 'btn btn-success';
        link.innerHTML = 'Zobacz folder';
        link.addEventListener('click', click.bind(this));

        elem.appendChild(titleElem);
        elem.appendChild(link);
      });
    }
  }, [map, folder]);

  const saveFolderPosition = () => {
    if (position) {
      PhotoFolderService.saveFolderPosition(position, folder).then(() => {
        console.log('Location saved');
      });
    }
  };

  return (
    <div>
      {/* Map and other UI elements can be added here */}
      <button onClick={saveFolderPosition}>Save Location</button>
    </div>
  );
};

export default MyFoldersCtrl;