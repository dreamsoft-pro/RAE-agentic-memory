import React, {useState} from 'react';
import ShowNotUsedPhotos from "./ShotNotUsedPhotosButton";
import ShowAllPhotosButton from "./ShowAllPhotosButton";


const UsedNotUsedImagesSwapper = ({data}) => {
    const [isAllPhotos, setIsAllPhotos] = useState(true);

    const handleClick = () => {
        setIsAllPhotos(prev => {
            if (prev) {
                $('#imagesList').addClass('displayNotUsedPhotos');
            } else {
                $('#imagesList').removeClass('displayNotUsedPhotos');
            }

            return !prev;
        });
    }

    return isAllPhotos ?
        (<ShowAllPhotosButton
            handleClick={handleClick}
            disabled={data.isUploading}
        />) :
        (<ShowNotUsedPhotos
            handleClick={handleClick}
            disabled={data.isUploading}
        />);
}

export default UsedNotUsedImagesSwapper;