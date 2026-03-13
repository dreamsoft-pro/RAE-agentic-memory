<?php

namespace DreamSoft\Controllers\AdminHelp;

use DreamSoft\Models\Lang\LangSetting;
use DreamSoft\Core\Controller;
use DreamSoft\Controllers\Components\Standard;
use DreamSoft\Models\AdminHelp\Help;
use DreamSoft\Models\AdminHelp\HelpLang;
use DreamSoft\Models\AdminHelp\HelpKey;

/**
 * Class HelpController
 */
class HelpController extends Controller
{
    protected $Help;
    protected $HelpLang;
    protected $LangSetting;
    protected $HelpKey;
    protected $Standard;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->Standard = Standard::getInstance();
        $this->Help = Help::getInstance();
        $this->LangSetting = LangSetting::getInstance();
        $this->HelpLang = HelpLang::getInstance();
        $this->HelpKey = HelpKey::getInstance();
    }

    public function setDomainID($domainID)
    {
        $this->domainID = $domainID;
        $this->LangSetting->setDomainID($domainID);
    }

    public function helps($module = null)
    {
        $lang = defined('lang') ? lang : 'pl';
        $data = strlen($module) > 0 ? $this->Help->getByModule($module, $lang) : $this->Help->getAll();
        return empty($data) ? [] : sort($data);
    }

    public function post_helps()
    {
        $module = $this->Data->getPost('module');
        $description = $this->Data->getPost('description');

        $return['response'] = false;

        if ($module) {
            if ($this->Help->exist('module', $module)) {
                return $this->sendFailResponse('08', 'Moduł ' . $module . ' już istnieje!');
            }

            $helpID = $this->Help->create(compact('module', 'description'));
            if ($helpID > 0) {
                $return = [
                    'response' => true,
                    'item' => $this->Help->get('ID', $helpID)
                ];
            }
        }
        return $return;
    }

    public function put_helps()
    {
        $post = $this->Data->getAllPost();
        $goodKeys = ['active', 'module', 'description'];
        $return['response'] = false;

        if (isset($post['ID']) && !empty($post['ID'])) {
            $ID = $post['ID'];
            unset($post['ID']);
            foreach ($post as $key => $value) {
                if (in_array($key, $goodKeys)) {
                    if ($key == 'module' && $this->Help->exist('module', $module)) {
                        return $this->sendFailResponse('08', 'Moduł ' . $module . ' już istnieje!');
                    }
                    $this->Help->update($ID, $key, $value);
                }
            }
            $return['response'] = true;
        }
        return $return;
    }

    public function delete_helps($ID)
    {
        $data = ['ID' => $ID, 'response' => false];
        $removeHL = 0;

        if (intval($ID) > 0 && $this->Help->delete('ID', $ID)) {
            $this->HelpKey->delete('moduleID', $ID);
            $all = $this->HelpKey->getByModule($ID);
            foreach ($all as $hk) {
                $removeHL += intval($this->HelpLang->delete('keyID', $hk['ID']));
            }
            $data['response'] = true;
            $data['removed'] = $ID;
            $data['removedTexts'] = 'removed: ' . $removeHL;
        }
        return $data;
    }

    public function keys($module, $key = '')
    {
        $data = [];
        if (strlen($module) > 0) {
            $data = strlen($key) > 0 ? $this->Help->getByParams($module, $key) : $this->Help->getByParams($module);
        }
        return empty($data) ? [] : $data;
    }

    public function post_keys($module)
    {
        $key = $this->Data->getPost('key');
        $moduleID = $this->Data->getPost('moduleID') ?: $this->Help->get('module', $module)['ID'];
        $texts = $this->Data->getPost('texts');
        $texts = is_array($texts) ? $texts : $this->Standard->objectToArray(json_decode($texts));

        if ($key && $moduleID) {
            if ($this->HelpKey->exist($moduleID, $key)) {
                return $this->sendFailResponse('08', 'Klucz: ' . $key . ' powtarza się dla modułu: ' . $moduleID);
            }

            $created = date('Y-m-d H:i:s');
            $lastID = $this->HelpKey->create(compact('key', 'moduleID', 'created'));
            $createdLang = 0;

            if ($lastID > 0) {
                $data = [
                    'item' => $this->HelpKey->get('ID', $lastID),
                    'response' => true,
                ];
                foreach ($texts as $lang => $t) {
                    $helpLangID = $this->HelpLang->exist($lang, $lastID);
                    if (intval($helpLangID) > 0) {
                        $this->HelpLang->update($helpLangID, 'description', $t['description']);
                        $this->HelpLang->update($helpLangID, 'title', $t['title']);
                    } else {
                        $params = [
                            'keyID' => $lastID,
                            'description' => $t['description'],
                            'title' => $t['title'],
                            'lang' => $lang
                        ];
                        $lastLangID = $this->HelpLang->create($params);
                        if ($lastLangID > 0) {
                            $data['item']['texts'][$lang] = [
                                'title' => $t['title'],
                                'description' => $t['description']
                            ];
                            $createdLang++;
                        }
                    }
                }
            } else {
                return $this->sendFailResponse('03');
            }
        } else {
            return $this->sendFailResponse('02');
        }
        $data['createdLang'] = $createdLang;
        return $data;
    }

    public function put_keys($module)
    {
        $post = $this->Data->getAllPost();
        $goodKeys = ['active', 'key'];
        $return['response'] = false;

        $moduleID = $this->Data->getPost('moduleID') ?: $this->Help->get('module', $module)['ID'];
        $texts = $this->Data->getPost('texts');
        $texts = is_array($texts) ? $texts : $this->Standard->objectToArray(json_decode($texts));
        $langs = $this->LangSetting->getAll();
        $langArr = array_column(array_filter($langs, fn($l) => $l['active'] == 1), 'code', 'code');

        if (isset($post['ID']) && !empty($post['ID'])) {
            $ID = $post['ID'];
            unset($post['ID']);
            foreach ($post as $key => $value) {
                if (in_array($key, $goodKeys)) {
                    if ($key == 'module' && $this->HelpKey->exist($moduleID, $key)) {
                        return $this->sendFailResponse('08', 'Klucz: ' . $key . ' powtarza się dla modułu: ' . $moduleID);
                    }
                    $this->Help->update($ID, $key, $value);
                    $return['item'] = $this->HelpKey->get('ID', $ID);
                }
            }
            $createdLang = 0;
            $updatedLang = 0;
            foreach ($texts as $lang => $t) {
                $helpLangID = $this->HelpLang->exist($lang, $ID);
                if (!isset($langArr[$lang])) {
                    $this->HelpLang->delete('ID', $helpLangID);
                    continue;
                }
                if (intval($helpLangID) > 0) {
                    $updatedLocal = intval($this->HelpLang->update($helpLangID, 'description', $t['description']));
                    $updatedLocal += intval($this->HelpLang->update($helpLangID, 'title', $t['title']));
                    if ($updatedLocal == 2) {
                        $updatedLang++;
                    }
                } else {
                    $params = [
                        'keyID' => $ID,
                        'description' => $t['description'],
                        'title' => $t['title'],
                        'lang' => $lang
                    ];
                    $lastLangID = $this->HelpLang->create($params);
                    if ($lastLangID > 0) {
                        $return['item']['texts'][$lang] = [
                            'title' => $t['title'],
                            'description' => $t['description']
                        ];
                        $createdLang++;
                    }
                }
            }
            $return['response'] = true;
            $return['updatedLang'] = $updatedLang;
            $return['createdLang'] = $createdLang;
        }
        return $return;
    }

    public function delete_keys($module, $ID)
    {
        $data = ['ID' => $ID, 'response' => false];
        if (intval($ID) > 0 && $this->HelpKey->delete('ID', $ID)) {
            $this->HelpLang->delete('keyID', $ID);
            $data['response'] = true;
            $data['removed'] = $ID;
        }
        return $data;
    }

    public function put_langs($module, $key)
    {
        $keyID = $this->Data->getPost('keyID') ?: $this->HelpKey->get('key', $key)['ID'];
        $texts = $this->Data->getPost('texts');
        $texts = is_array($texts) ? $texts : $this->Standard->objectToArray(json_decode($texts));
        $langs = $this->LangSetting->getAll();
        $langArr = array_column(array_filter($langs, fn($l) => $l['active'] == 1), 'code', 'code');
        $saved = 0;
        $updated = 0;

        if ($keyID && !empty($texts)) {
            foreach ($texts as $lang => $d) {
                if (isset($langArr[$lang])) {
                    $exist = $this->HelpLang->exist($lang, $keyID);
                    if (!$exist) {
                        $params = [
                            'keyID' => $keyID,
                            'description' => $d['description'],
                            'title' => $d['title'],
                            'lang' => $lang
                        ];
                        $lastID = $this->HelpLang->create($params);
                        if ($lastID > 0) {
                            $saved++;
                        }
                    } else {
                        $updatedLocal = intval($this->HelpLang->update($exist, 'description', $d['description']));
                        $updatedLocal += intval($this->HelpLang->update($exist, 'title', $d['title']));
                        if ($updatedLocal == 2) {
                            $updated++;
                        }
                    }
                }
            }
            return [
                'response' => true,
                'saved' => $saved,
                'updated' => $updated
            ];
        }
        return $this->sendFailResponse('02');
    }
}
