<?php

/**
 * Created by PhpStorm.
 * User: rafal
 * Date: 23.01.17
 * Time: 23:33
 */

namespace DreamSoft\Controllers\Addresses;

use DreamSoft\Core\Controller;
use DreamSoft\Models\Address\Address;
use DreamSoft\Models\Address\AddressUser;
use DreamSoft\Models\User\User;

class AddressesController extends Controller
{
    public $useModels = [];

    /**
     * @var Address
     */
    protected $Address;
    /**
     * @var User
     */
    protected $User;
    /**
     * @var AddressUser
     */
    private $AddressUser;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->Address = Address::getInstance();
        $this->User = User::getInstance();
        $this->AddressUser = AddressUser::getInstance();
    }

    public function address($userID, $params)
    {
        $address = $this->Address->getDefault($userID, $params['type']);

        if (!$address) {
            return ['response' => true, 'address' => []];
        }

        return ['response' => true, 'address' => $address];
    }

    /**
     * @param int $type
     * @return array
     */
    public function getAddress($type = 1)
    {
        $loggedUser = $this->Auth->getLoggedUser();
        if (!$loggedUser) {
            return ['response' => false, 'address' => []];
        }

        $userInfo = $this->User->get('ID', $loggedUser['ID']);
        $user = ['login' => $userInfo['login']];
        $address = $this->Address->getDefault($loggedUser['ID'], $type);

        if (!$address) {
            return ['response' => true, 'address' => []];
        }

        return [
            'response' => true,
            'address' => $address,
            'user' => $user
        ];
    }

    /**
     * @param $addressID
     * @return mixed
     */
    public function patch_updateAddress($addressID)
    {
        $loggedUser = $this->Auth->getLoggedUser();
        if (!$loggedUser) {
            return $this->sendFailResponse('17');
        }

        $type = $this->Data->getPost('type');
        if (!$addressID && $type == 2) {
            return $this->post_addAddress($type);
        }

        $join = $this->Address->getJoin($addressID, $loggedUser['ID']);
        if (!$join) {
            return $this->sendFailResponse('14');
        }

        $post = $this->Data->getAllPost();
        $goodFields = [
            'name', 'lastname', 'street', 'house', 'apartment', 'zipcode',
            'city', 'areaCode', 'telephone', 'companyName', 'nip', 'addressName', 'countryCode'
        ];

        if (!empty($post)) {
            $saved = 0;
            foreach ($post as $key => $value) {
                if (in_array($key, $goodFields)) {
                    $saved = intval($this->Address->update($addressID, $key, $value));
                }
            }

            if ($saved > 0) {
                if (intval($post['default']) > 0) {
                    $addressUserEntity = $this->AddressUser->get('addressID', $addressID);
                    if ($addressUserEntity) {
                        if ($addressUserEntity['default'] != 1) {
                            $this->AddressUser->resetDefault($addressUserEntity['userID'], $addressUserEntity['type']);
                            if ($this->AddressUser->update($addressUserEntity['ID'], 'default', 1)) {
                                $data['defaultAddressChanged'] = true;
                            }
                        }
                        $this->User->update($addressUserEntity['userID'], 'name', $post['name']);
                        $this->User->update($addressUserEntity['userID'], 'lastname', $post['lastname']);
                    }
                }

                $data['response'] = true;
                $data['info'] = 'Saved: ' . count($post) . ' fields.';
                $data['item'] = $this->Address->getOne($addressID);
            } else {
                $data = $this->sendFailResponse('03');
            }
        } else {
            $data = $this->sendFailResponse('01');
        }

        return $data;
    }

    /**
     * @param int $type
     * @return array|bool
     */
    public function getAddresses($type = 1)
    {
        $loggedUser = $this->Auth->getLoggedUser();
        if (!$loggedUser) {
            return $this->sendFailResponse('17');
        }

        $addresses = $this->Address->customGetAll($loggedUser['ID'], $type);
        return $addresses ?: [];
    }

    public function post_addAddress($type = 1)
    {
        $loggedUser = $this->Auth->getLoggedUser();
        if (!$loggedUser) {
            return $this->sendFailResponse('17');
        }

        $data['response'] = false;

        $address = [
            'addressName' => $this->Data->getPost('addressName'),
            'name' => $this->Data->getPost('name'),
            'lastname' => $this->Data->getPost('lastname'),
            'companyName' => $this->Data->getPost('companyName'),
            'street' => $this->Data->getPost('street'),
            'house' => $this->Data->getPost('house'),
            'apartment' => $this->Data->getPost('apartment'),
            'zipcode' => $this->Data->getPost('zipcode'),
            'city' => $this->Data->getPost('city'),
            'areaCode' => $this->Data->getPost('areaCode'),
            'telephone' => $this->Data->getPost('telephone'),
            'countryCode' => $this->Data->getPost('countryCode'),
            'nip' => $this->Data->getPost('nip')
        ];

        $default = $this->Data->getPost('default') ? 1 : 0;

        if (strlen($address['addressName']) == 0) {
            $address['addressName'] = $address['city'] . ' - ' . $address['street'] . ' ' . $address['house'];
            if (strlen($address['apartment']) > 0) {
                $address['addressName'] .= '/' . $address['apartment'];
            }
        }

        $addressID = $this->Address->create($address);
        if (intval($addressID) > 0) {
            $params = [
                'type' => $type,
                'userID' => $loggedUser['ID'],
                'addressID' => $addressID,
                'default' => $default
            ];
            $joinAddressID = $this->Address->createJoin($params);
        } else {
            return $this->sendFailResponse('03');
        }

        if ($addressID && $joinAddressID) {
            $data['response'] = true;
            $data['info'] = 'Saved address. ID: ' . $addressID;
            $data['item'] = $this->Address->getOne($addressID);
        }

        return $data;
    }

    /**
     * @return array
     */
    public function emptyAddress()
    {
        return ['response' => true];
    }

    /**
     * @param $addressID
     * @return array
     */
    public function delete_address($addressID)
    {
        $loggedUser = $this->Auth->getLoggedUser();
        if (!$loggedUser) {
            return $this->sendFailResponse('17');
        }

        $addressUserEntities = $this->AddressUser->get('addressID', $addressID, true);
        foreach ($addressUserEntities as $addressUserRow) {
            if (intval($addressUserRow['default']) == 1) {
                return ['response' => false, 'info' => 'address_is_default'];
            }
            if ($addressUserRow['userID'] != $loggedUser['ID']) {
                return ['response' => false, 'info' => 'user_not_own_this_address'];
            }
        }

        if ($this->Address->delete('ID', $addressID) && $this->AddressUser->delete('addressID', $addressID)) {
            return ['response' => true, 'info' => 'address_removed'];
        }

        return ['response' => false, 'info' => 'error'];
    }
}
