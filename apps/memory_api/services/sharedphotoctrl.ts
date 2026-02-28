javascript
import { PhotoFolderService } from '@/lib/api';

export const getPhotoSharedByEmail = (photoId, password) => {
    return PhotoFolderService.getPhotoSharedByEmail(photoId, password).then(data => {
        return data;
    });
};

// [BACKEND_ADVICE] Consider moving heavy logic to backend if necessary.

export const updateScopeWithPhoto = async ($scope, photoId, password) => {
    try {
        $scope.photo = await getPhotoSharedByEmail(photoId, password);
    } catch (error) {
        console.error('Failed to load photo:', error);
    }
};

export const selectPhoto = ($scope, photo) => {
    $scope.actualPhoto = photo;
};
