<?php
namespace DreamSoft\Controllers\Components;

use DreamSoft\Core\Component;
use DreamSoft\Models\PrintShopProduct\PrintShopFormat;
use DreamSoft\Models\Lang\LangSetting;
use DreamSoft\Models\PrintShopProduct\PrintShopPrintTypeWorkspace;
use DreamSoft\Models\PrintShop\PrintShopComplex;
use DreamSoft\Models\PrintShop\PrintShopComplexRelatedFormat;

/**
 * Class FormatAssistant
 * This class provides methods for handling format-related operations.
 * Methods were updated to use PHP 8+ language features and improve code maintainability and readability.
 * No functionality or method/function names have been changed.
 */
class FormatAssistant extends Component
{
    private PrintShopFormat $PrintShopFormat;
    private LangSetting $LangSetting;
    private Standard $Standard;
    private PrintShopPrintTypeWorkspace $PrintShopPrintTypeWorkspace;
    private PrintShopComplex $PrintShopComplex;
    private PrintShopComplexRelatedFormat $PrintShopComplexRelatedFormat;

    /**
     * FormatAssistant constructor.
     * Initializes required objects using singleton pattern methods.
     */
    public function __construct()
    {
        parent::__construct();
        $this->PrintShopFormat = PrintShopFormat::getInstance();
        $this->LangSetting = LangSetting::getInstance();
        $this->Standard = Standard::getInstance();
        $this->PrintShopPrintTypeWorkspace = PrintShopPrintTypeWorkspace::getInstance();
        $this->PrintShopComplex = PrintShopComplex::getInstance();
        $this->PrintShopComplexRelatedFormat = PrintShopComplexRelatedFormat::getInstance();
    }

    /**
     * Returns format data based on provided arguments.
     * 
     * @param int      $groupID   // Group identifier
     * @param int      $typeID    // Type identifier
     * @param int|null $complexID // Complex identifier, can be null
     * @param int|null $ID        // Format ID, can be null
     * @param int      $public    // Public flag
     * @return array
     */
    public function formats(int $groupID, int $typeID, ?int $complexID = null, ?int $ID = null, int $public = 0): array
    {
        // Set initial parameters
        $this->PrintShopFormat->setGroupID($groupID);
        $this->PrintShopFormat->setTypeID($typeID);

        // If a specific format ID is provided
        if (($ID ?? 0) > 0) {
            $data = $this->PrintShopFormat->getOne($ID);
        } else {
            // Fetch data depending on the 'public' parameter
            $data = $public === 1 
                ? $this->PrintShopFormat->getAll(1) 
                : $this->PrintShopFormat->getAll();

            $allIDs = [];

            if (!empty($data)) {
                // Fill each format with default language name if not present
                $data = $this->fillWithDefaultLangName($data);

                // Process print types and convert units if necessary
                foreach ($data as $key => $val) {
                    $allIDs[] = $val['ID'];

                    // Split print types from a semicolon-delimited string
                    $exp = explode(';', $val['printTypesList'] ?? '');
                    
                    // Build array of print types
                    foreach ($exp as $e) {
                        // Skip empty entries
                        if (strlen($e) === 0) {
                            continue;
                        }
                        $exp2 = explode(':', $e);
                        $volumes = $exp2[1] ?? '';
                        $volumesArr = explode('-', $volumes);

                        // Assign min and max volumes
                        $minVolume = $volumesArr[0] ?? null;
                        $maxVolume = $volumesArr[1] ?? null;

                        $data[$key]['printTypes'][] = [
                            'printTypeID' => $exp2[0],
                            'minVolume'   => $minVolume,
                            'maxVolume'   => $maxVolume
                        ];
                    }

                    // Make sure printTypes is an array even if empty
                    if (empty($data[$key]['printTypes'])) {
                        $data[$key]['printTypes'] = [];
                    }

                    // Convert dimensions if unit == 2
                    if (isset($val['unit']) && $val['unit'] == 2) {
                        // Use an array of fields to reduce repetitive calls
                        $fields = [
                            'height', 'width', 'slope', 
                            'maxHeight', 'maxWidth', 
                            'minHeight', 'minWidth'
                        ];
                        foreach ($fields as $field) {
                            $data = $this->Standard->convertToCentimeter($data, $key, $field);
                        }
                    }
                    unset($data[$key]['printTypesList']);
                }

                // Check workspaces for each format & print type
                $data = $this->checkPrintTypeWorkspacesExist($data);

                // If a complex ID is provided, retrieve and attach related formats
                $complex = $complexID ? $this->PrintShopComplex->getBase($complexID) : null;
                if ($complex) {
                    $typesComplex = $this->PrintShopComplex->getByBaseID($complex['baseID'], $complex['complexGroupID']);
                    $typesArr = [];

                    if ($typesComplex) {
                        foreach ($typesComplex as $tc) {
                            // Build an array of type IDs different than the currently used typeID
                            if ($tc['typeID'] != $typeID) {
                                $typesArr[] = $tc['typeID'];
                            }
                        }
                    }

                    // Retrieve related formats or default to an empty array if null
                    $relatedFormats = $this->PrintShopComplexRelatedFormat->getByBaseFormatIDs($allIDs, $typesArr, $complex['ID']) ?? [];

                    // If $relatedFormats is valid, group them by 'baseFormatID'
                    if (is_array($relatedFormats) && !empty($relatedFormats)) {
                        $rf = [];

                        // Group related formats
                        foreach ($relatedFormats as $relatedFormat) {
                            // Ensure 'baseFormatID' is set
                            if (!isset($relatedFormat['baseFormatID'])) {
                                continue;
                            }
                            $formatID = $relatedFormat['baseFormatID'];
                            $rf[$formatID][] = $relatedFormat;
                        }

                        // Attach related formats to the $data array
                        foreach ($data as $key => $val) {
                            if (isset($val['ID']) && isset($rf[$val['ID']])) {
                                $data[$key]['relatedFormats'] = $rf[$val['ID']];
                            }
                        }
                    }
                }
            }
        }

        return $data;
    }

    /**
     * Fills each format with a default language name if none is set for the given active languages.
     *
     * @param array $formats
     * @return array
     */
    public function fillWithDefaultLangName(array $formats): array
    {
        $languages = $this->LangSetting->getAll();
        if ($languages) {
            // Filter only active languages
            $activeLanguages = array_filter($languages, fn($lang) => $lang['active'] == 1);

            // Iterate over formats
            foreach ($formats as $key => $format) {
                // For each active language, set default name if not present
                foreach ($activeLanguages as $al) {
                    if (empty($format['langs'][$al['code']])) {
                        $formats[$key]['langs'][$al['code']]['name'] = $format['name'];
                    }
                }
            }
        }
        return $formats;
    }

    /**
     * Checks whether the print type workspaces exist for each format's print types.
     * 
     * @param array $data
     * @return array
     */
    private function checkPrintTypeWorkspacesExist(array $data): array
    {
        // If $data is empty, return immediately
        if (!$data) {
            return $data;
        }

        // Collect format IDs
        $formatsAggregate = array_column($data, 'ID');

        // Collect all printTypeIDs
        $printTypesAggregate = array_reduce($data, function ($carry, $row) {
            $printTypeIDs = array_column($row['printTypes'] ?? [], 'printTypeID');
            return array_merge($carry, $printTypeIDs);
        }, []);

        // Get data from PrintShopPrintTypeWorkspace
        $printTypeWorkspaces = $this->PrintShopPrintTypeWorkspace
            ->getByAggregateData($printTypesAggregate, $formatsAggregate);

        // Check if each format's print type workspace exists
        foreach ($data as $formatKey => $row) {
            foreach ($row['printTypes'] as $printTypeKey => $printType) {
                $data[$formatKey]['printTypes'][$printTypeKey]['printTypeWorkspaceExist'] =
                    !empty($printTypeWorkspaces[$row['ID']][$printType['printTypeID']]);
            }
        }

        return $data;
    }

    /**
     * Placeholder method for retrieving selected options if needed.
     * 
     * Currently not implemented, returns void.
     */
    private function getSelectedOptions(): void
    {
        // To be implemented if needed
    }
}
