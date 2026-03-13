
import React, { useState } from 'react';
import './styles.css'; // Assuming you have a styles file with your Tailwind configurations

type ProductType = {
  calcProducts: { pages: number }[];
  fileList: Array<{ minUrl?: string; volume?: number }>;
};

type AttrDataType = {
  doubleSidedSheet?: number;
  attrID?: number;
  calcProductID?: number;
  cpAttrID?: number;
};

const UploadFilesButton: React.FC<{
  product: ProductType;
  file: { minUrl?: string; volume?: number };
  attrData: AttrDataType;
}> = ({ product, file, attrData }) => {
  const [isSideAssign] = useState(() =>
    isDoubleSided(product.calcProducts[0].pages > 2 ? false : true, attrData)
  );

  const formatSizeUnits = (bytes) => {
    // Assuming MainWidgetService.formatSizeUnits(bytes) exists and returns a formatted string.
    return 'formatted size'; // Replace with actual implementation
  };

  const isDoubleSided = (pages: boolean, attrData: AttrDataType): boolean => {
    if (!pages && attrData.doubleSidedSheet === 1) {
      return true;
    }
    for (let i = 0; i < product.fileList.length; i++) {
      if (attrData.doubleSidedSheet === 1 && attrData.attrID == 1) {
        return true;
      }
    }
    return false;
  };

  const uploadFiles = () => {
    // Your implementation for uploading files
    console.log('Uploading Files...');
  };

  return (
    <table className="w-full">
      <tbody>
        <tr key={file.volume}>
          <td>
            {!file.minUrl && isSideAssign ? (
              <button
                onClick={() => uploadFiles()}
                className="btn btn-s btn-block btn-info"
                title="files"
              >
                <i className="fa fa-plus"></i> Add File
              </button>
            ) : null}
          </td>
        </tr>
      </tbody>
    </table>
  );
};

export default UploadFilesButton;
