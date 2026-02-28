javascript
// [BACKEND_ADVICE] Consider moving heavy logic to the backend if necessary.

import { getImageDownloadSrc, changeImage, nextImage, prevImage } from '@/lib/api';

scope.getImageDownloadSrc = () => {
    const image = scope.images[scope.index];
    return image ? image.downloadSrc : null;
};

scope.changeImage = (i) => {
    scope.index = i;
    showImage(i);
};

scope.nextImage = () => {
    scope.index += 1;
    if (scope.index === scope.images.length) {
        scope.index = 0;
    }
    showImage(scope.index);
};

scope.prevImage = () => {
    scope.index -= 1;
    if (scope.index < 0) {
        scope.index = scope.images.length - 1;
    }
    showImage(scope.index);
};
