javascript
// [BACKEND_ADVICE] This function updates the average rating for a folder or photo.
import { updateFolderAverageRate, updatePhotoAverageRate } from '@/lib/api';

function updateRate(scope, id, rate) {
    console.log(scope);
    if (scope.type === 'folder') {
        updateFolderAverageRate(scope.$parent.folder._id, rate)
            .then(() => scope.$parent.folder.averageRate = rate);
    } else if (scope.type === 'photo') {
        const photoIndex = _.findIndex(scope.$parent.photos, {_id: id});
        if (photoIndex > -1) {
            updatePhotoAverageRate(id, rate)
                .then(() => scope.$parent.photos[photoIndex].averageRate = rate);
        }
    }
}
