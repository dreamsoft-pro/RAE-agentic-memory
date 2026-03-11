javascript
import { BackendApi } from '@/lib/api';
import { PhotoFolderService } from '@/services/photo-folder-service';

export const SharedFolderCtrl = {
    onInit: function ($stateParams, notificationService) {
        this.actualPhoto = {};
        this.folderId = $stateParams.folderid;
        this.source = $stateParams.source;
        this.folder = {};
        this.photos = [];

        this.rating = {
            current: 0,
            max: 5
        };

        // [BACKEND_ADVICE] This should be handled by the backend service.
        this.getSelectedRating = function (rating) {
            console.log(rating);
        };

        this.init();
    },

    init: function () {
        BackendApi.getFolder(this.folderId).then((folderData) => {
            this.folder = folderData;
            return BackendApi.getPhotosInFolder(this.folderId, this.source);
        }).then((photosData) => {
            this.photos = photosData;
        }).catch((error) => {
            notificationService.error('Failed to load data', error.message);
        });
    }
};
