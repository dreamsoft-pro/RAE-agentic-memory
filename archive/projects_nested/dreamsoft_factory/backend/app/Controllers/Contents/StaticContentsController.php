<?php
/**
 * Programista Rafał Leśniak - 19.6.2017
 */

namespace DreamSoft\Controllers\Contents;

use DreamSoft\Models\Content\StaticContent;
use DreamSoft\Models\Content\StaticContentLang;
use DreamSoft\Core\Controller;

class StaticContentsController extends Controller
{
    protected $StaticContent;
    protected $StaticContentLang;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->StaticContent = StaticContent::getInstance();
        $this->StaticContentLang = StaticContentLang::getInstance();
    }

    public function setDomainID($domainID)
    {
        $this->StaticContent->setDomainID($domainID);
        parent::setDomainID($domainID);
    }

    public function index()
    {
        $data = $this->StaticContent->getAll();
        if (!$data) {
            return [];
        }

        foreach ($data as $key => $row) {
            $data[$key]['forDomain'] = $row['domainID'] > 0 ? 1 : 0;
        }

        return $data;
    }

    public function post_index()
    {
        $post = $this->Data->getAllPost();
        $data['response'] = false;

        if (empty($post['contents'])) {
            return $this->sendFailResponse('01');
        }

        if (!empty($post) && isset($post['key'])) {
            if ($this->StaticContent->get('key', $post['key'])) {
                return $this->sendFailResponse('08');
            }

            $params = [
                'key' => $post['key'],
                'domainID' => intval($post['forDomain']) == 1 ? $this->getDomainID() : null
            ];
            $lastContentID = $this->StaticContent->create($params);

            $langSaved = [];
            foreach ($post['contents'] as $lang => $content) {
                $params = [
                    'lang' => $lang,
                    'content' => $content,
                    'staticContentID' => $lastContentID
                ];
                $langSaved[] = $this->StaticContentLang->create($params);
            }

            if ($lastContentID > 0) {
                $data = [
                    'response' => true,
                    'langSaved' => $langSaved,
                    'one' => $this->StaticContent->getOne($lastContentID) + ['forDomain' => $params['domainID'] > 0 ? 1 : 0]
                ];
            }
        } else {
            return $this->sendFailResponse('01');
        }

        return $data;
    }

    public function put_index()
    {
        $post = $this->Data->getAllPost();
        $data['response'] = false;

        if (!empty($post) && isset($post['key'])) {
            $staticContent = $this->StaticContent->get('ID', $post['ID']);

            $updated = intval($this->StaticContent->update($staticContent['ID'], 'key', $post['key']));
            if (isset($post['forDomain'])) {
                $domainID = intval($post['forDomain']) > 0 ? $this->getDomainID() : NULL;
                $updated += intval($this->StaticContent->update($staticContent['ID'], 'domainID', $domainID));
            }
            if (isset($post['active'])) {
                $updated += intval($this->StaticContent->update($staticContent['ID'], 'active', intval($post['active']) > 0 ? 1 : 0));
            }

            $params = [];
            $updatedLangs = $deleted = $added = 0;
            foreach ($post['contents'] as $lang => $content) {
                $existID = $this->StaticContentLang->exist($staticContent['ID'], $lang);
                if ($existID) {
                    if (strlen($content) > 0) {
                        $updatedLangs += intval($this->StaticContentLang->update($existID, 'content', $content));
                    } else {
                        $deleted += intval($this->StaticContentLang->delete('ID', $existID));
                    }
                } else {
                    $params = [
                        'lang' => $lang,
                        'content' => $content,
                        'staticContentID' => $staticContent['ID']
                    ];
                    if ($this->StaticContentLang->create($params) > 0) {
                        $added++;
                    }
                }
            }

            $allActions = $updated + $updatedLangs + $deleted + $added;
            if ($allActions > 0) {
                $data = [
                    'response' => true,
                    'updated' => $updated,
                    'updatedLangs' => $updatedLangs,
                    'deleted' => $deleted,
                    'added' => $added,
                    'one' => $this->StaticContent->getOne($staticContent['ID']) + ['forDomain' => $staticContent['domainID'] > 0 ? 1 : 0]
                ];
                return $data;
            }
        }

        return $data;
    }

    public function delete_index($ID)
    {
        $data['response'] = false;
        if ($ID && $this->StaticContent->delete('ID', $ID)) {
            $this->StaticContentLang->delete('staticContentID', $ID);
            $data['response'] = true;
        } else {
            $data = $this->sendFailResponse('04');
        }

        return $data;
    }

    public function getContent($key)
    {
        $data = $this->StaticContent->getByKey($key);

        if (!$data || ($data['domainID'] != $this->getDomainID() && $data['domainID'] != NULL)) {
            return ['return' => false];
        }

        return $data;
    }
}
