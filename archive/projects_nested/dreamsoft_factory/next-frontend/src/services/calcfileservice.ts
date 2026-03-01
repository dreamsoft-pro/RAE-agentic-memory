javascript
import { backendApi } from '@/lib/api';

CalcFileService.editImage = function (fileID, data) {
    const promise = backendApi.post(['calcFilesUploader', 'editImage', fileID].join('/'), data)
        .then(response => response.data)
        .catch(error => Promise.reject(error));

    return promise;
};

export { CalcFileService };
