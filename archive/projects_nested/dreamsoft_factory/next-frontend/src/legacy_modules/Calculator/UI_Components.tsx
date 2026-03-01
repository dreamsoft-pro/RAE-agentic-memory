import { $q } from './httpBridge';
/**
 */

import React from "react";
import { useCalculator } from "../CalculatorContext";

export const UI_Components = () => {
  const calc = useCalculator();


  // --- chunk_004.tsx ---







const GalleryComponent: React.FC = () => {
    const [galleries, setGalleries] = useState<any[]>([]);
    const [sliderData, setSliderData] = useState<any[]>([]);
    const [thumbnails, setThumbnails] = useState<any[]>([]);
    const [patterns, setPatterns] = useState<any[]>([]);
    const router = useRouter();
    const dispatch = useDispatch();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('/api/data');
                const data = response.data;

                if (data) {
                    data.forEach((oneDesc: any) => {
                        switch (oneDesc.type) {
                            case 5:
                                oneDesc.items = [];
                                if (!_.isEmpty(oneDesc.files)) {
                                    _.each(oneDesc.files, (oneFile) => {
                                        oneDesc.items.push({
                                            thumb: oneFile.urlCrop,
                                            img: oneFile.url,
                                            description: `Image ${oneFile.fileID}`
                                        });
                                    });
                                }
                                setGalleries((prevGalleries) => [...prevGalleries, oneDesc]);
                                break;
                            case 3:
                                setSliderData((prevSliderData) => [...prevSliderData, oneDesc]);
                                break;
                            case 6:
                                setThumbnails((prevThumbnails) => [...prevThumbnails, oneDesc]);
                                break;
                            case 7:
                                setPatterns(oneDesc.patterns);
                                break;
                        }
                    });
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <div>
            {/* Render your components here */}
        </div>
    );
};

export default GalleryComponent;
  // --- chunk_005.tsx ---





const getType = async (groupUrl: string, typeUrl: string) => {
  const response = await PsTypeService.getOneForView(groupUrl, typeUrl);
  if (response && response.active === 0) {
    Notification.error($filter('translate')('product_currently_not_available'));
    $state.go('home');
    return;
  }
  calc.currentGroupID = response.groupID;
  calc.currentTypeID = response.ID;
  calc.autoselect = response.autoselect;
  MainWidgetService.includeTemplateVariables(calc, 'calc', calc.currentGroupID, calc.currentTypeID);
  calc.type = response;

  if ($rootScope.logged === false) {
    const calcFilesSetID = localStorageService.get('calcFilesSetID');
    if (!calcFilesSetID) {
      const createGuestSetResponse = await CalcFileService.createGuestSet(calc.type.ID);
      calc.calcFilesSetID = createGuestSetResponse?.response ? createGuestSetResponse.calcFileSetID : null;
      localStorageService.set('calcFilesSetID', calc.calcFilesSetID);
    } else {
      const caclFilesData = await CalcFileService.getBySetID(calcFilesSetID);
      calc.calcFiles = caclFilesData;
      calc.setPagination(calc.calcFilesCurrentPage);
    }
  } else {
    const caclFilesData = await CalcFileService.getAllByType(calc.type.ID);
    calc.calcFiles = caclFilesData;
    calc.setPagination(calc.calcFilesCurrentPage);
  }
};

const ComplexGroupLoader: React.FC = () => {
  const { loading, error, data } = useQuery(GET_COMPLEX_GROUP);

  useEffect(() => {
    if (!loading && !error) {
      // Assuming `data` contains the necessary group and type information
      const promises: Promise<any>[] = [];

      for (const type of data.types) {
        const group = {
          ID: null,
          name: type.name,
          names: type.names,
          productID: type.ID,
          type: "other",
          products: []
        };

        const product = {
          groupID: type.groupID,
          typeID: type.ID,
          typeName: type.name,
          typeNames: type.names
        };

        group.products.push(product);
        promises.push(calc.getComplexGroup(group, 1));
      }

      $q.all(promises).then(() => {
        getFormat();
        log.info('100% - loaded');
        updateLinkToCopy();
        setupClipboardJS();
        DomWidgetService.pinElementWhenScroll(".panel-summary", ".panel-summary .panel-heading", ".panel-configuration");
      }).catch((data) => {
        console.error('ERR: Problem with products load', data);
      });
    }
  }, [loading, error, data]);

  return <div>Loading...</div>;
};

export default ComplexGroupLoader;
};
