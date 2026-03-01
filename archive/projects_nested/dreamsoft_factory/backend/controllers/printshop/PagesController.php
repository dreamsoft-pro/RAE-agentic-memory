<?php

use DreamSoft\Models\PrintShopProduct\PrintShopPageName;
use DreamSoft\Models\PrintShopProduct\PrintShopPage;
use DreamSoft\Core\Controller;

class PagesController extends Controller
{
    public $useModels = array();
    protected $PrintShopPage;
    protected $PrintShopPageName;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopPage = PrintShopPage::getInstance();
        $this->PrintShopPageName = PrintShopPageName::getInstance();
    }

    public function pages($groupID, $typeID, $ID = NULL)
    {
        $this->PrintShopPage->setGroupID($groupID);
        $this->PrintShopPage->setTypeID($typeID);

        $data = intval($ID) > 0 ? $this->PrintShopPage->get('ID', $ID) : $this->PrintShopPage->getAll();
        return $data ?: array();
    }

    public function pagesPublic($groupID, $typeID, $ID = NULL)
    {
        return $this->pages($groupID, $typeID, $ID);
    }

    public function patch_pages($groupID, $typeID)
    {
        $this->PrintShopPage->setGroupID($groupID);
        $this->PrintShopPage->setTypeID($typeID);

        $action = $this->Data->getPost('action');
        $data['response'] = false;

        try {
            switch ($action) {
                case 'pages':
                    $pages = $this->Data->getPost('pages');
                    if ($pages) {
                        $lastID = $this->PrintShopPage->customCreate($pages);
                        $data['response'] = $lastID > 0;
                        $data['item'] = $lastID > 0 ? $this->PrintShopPage->get('ID', $lastID) : null;
                    }
                    break;
                case 'range':
                    $minPages = $this->Data->getPost('minPages');
                    $maxPages = $this->Data->getPost('maxPages');
                    $step = $this->Data->getPost('step');
                    $doublePage = $this->Data->getPost('doublePage') ?: 0;

                    if ($minPages && $maxPages && $step) {
                        $lastID = $this->PrintShopPage->createRange($minPages, $maxPages, $step, $doublePage);
                        $data['response'] = $lastID > 0;
                        $data['item'] = $lastID > 0 ? $this->PrintShopPage->get('ID', $lastID) : null;
                    } else {
                        $data['error'] = "Required parameters missing (minPages=$minPages, maxPages=$maxPages, step=$step)";
                    }
                    break;
                case 'similarPage':
                    $similarPage = $this->Data->getPost('similarPage');
                    $data['response'] = $this->PrintShopPage->setPagesSimilar($similarPage);
                    break;
            }
        } catch (Exception $ex) {
            $data['error'] = $ex->getMessage();
        }

        return $data;
    }

    public function delete_pages($groupID, $typeID, $ID)
    {
        $data['response'] = false;

        if (intval($ID) > 0) {
            try {
                $data['response'] = $this->PrintShopPage->delete('ID', $ID);
            } catch (Exception $ex) {
                $data['error'] = $ex->getMessage();
            }
        } else {
            header("HTTP/1.0 403 Forbidden");
        }

        return $data;
    }

    public function customName($typeID)
    {
        $customNames = $this->PrintShopPageName->getByType($typeID);
        return $this->prepareCustomNames($customNames);
    }

    private function prepareCustomNames($data)
    {
        $list = array();
        if ($data) {
            foreach ($data as $row) {
                $list[$row['lang']] = $row['name'];
            }
        }
        return $list;
    }

    public function patch_customName($typeID)
    {
        $post = $this->Data->getAllPost();
        $return['response'] = false;

        if ($post['names'] === NULL) {
            return $this->sendFailResponse('02');
        }

        $updated = $saved = $deleted = 0;

        if (empty($post['names'])) {
            $deleted += $this->PrintShopPageName->delete('typeID', $typeID);
        }

        foreach ($post['names'] as $lang => $name) {
            $existPageNameID = $this->PrintShopPageName->nameExist($typeID, $lang);
            if ($existPageNameID) {
                if (strlen($name) == 0) {
                    $deleted += $this->PrintShopPageName->delete('ID', $existPageNameID);
                } else {
                    $updated += $this->PrintShopPageName->update($existPageNameID, 'name', $name);
                }
            } else {
                $params = compact('lang', 'name', 'typeID');
                $lastID = $this->PrintShopPageName->create($params);
                if ($lastID > 0) {
                    $saved++;
                }
            }
        }

        if (($updated + $saved + $deleted) > 0) {
            $return['response'] = true;
            $return['saved'] = $saved;
            $return['updated'] = $updated;
            $return['deleted'] = $deleted;
            $customNames = $this->PrintShopPageName->getByType($typeID);
            $return['customNames'] = $this->prepareCustomNames($customNames);
        }

        return $return;
    }
}
