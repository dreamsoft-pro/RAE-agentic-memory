javascript
import '@/lib/api';

uploader.onSuccessItem = async (fileItem, response, status, headers) => {
    response.file.size = (fileItem._file.size / 1024).toFixed(2);
    product.fileList.push(response.file);

    // [BACKEND_ADVICE] Heavy logic to make miniature
    const responseMiniature = await ProductFileService.makeMiniature(response.file.ID);
    
    if (responseMiniature.response === true) {
        const fileIdx = _.findIndex(product.fileList, { ID: response.file.ID });
        if (fileIdx > -1) {
            product.fileList[fileIdx].minUrl = responseMiniature.minUrl;
            product.fileList[fileIdx].hasMiniature = true;
        }
    }

    product.lastFile = response.file;
};
