<?php

use DreamSoft\Controllers\Components\Acl;
use DreamSoft\Models\Mongo\MgSession;
use DreamSoft\Core\Controller;
use DreamSoft\Libs\JWT;
use DreamSoft\Models\User\User;

class AuthController extends Controller {
    /**
     * @var MgSession
     */
    protected $MgSession;
    /**
     * @var Acl
     */
    protected $Acl;
    /**
     * @var User
     */
    protected $User;

    public $useModels = array();

    public function __construct($params) {
        parent::__construct($params);
        $this->User = User::getInstance();
        $this->MgSession = MgSession::getInstance();
        $this->Acl = new Acl();
    }

    public function setDomainID($domainID) {
        parent::setDomainID($domainID);
        $this->User->setDomainID($domainID);
    }
    
    protected function _firstCheck() {
        if (!$this->Auth->checkLogin()) {
            $data['reason'] = 'Brak ID użytkownika w sesji';
            header("HTTP/1.0 401 Unauthorized");
            $data['response'] = false;
        } else {
            $user = $this->Auth->getLoggedUser();
            $data['user'] = array(
                'firstname' => $user['firstname'] ?? null,
                'lastname' => $user['lastname'] ?? null,
                'mail' => $user['user'] ?? $user['login'] ?? null,
            );
            if ($token = $this->Auth->getToken()) {
                $data[ACCESS_TOKEN_NAME] = $token;
            }
            $data['response'] = true;
            $data['domainID'] = $this->getDomainID();
        }
        return $data;
    }

    protected function _secondCheck() {
        $token = $this->Auth->getToken();
        $data['response'] = false;
        if (strlen($token) > 0) {
            try {
                $decode = JWT::decode($token, secretKey, array('HS256'));
            } catch (Exception $ex) {
                $data['error'] = $ex->getMessage();
                header("HTTP/1.0 401 Unauthorized");
                return $data;
            }

            $mongoSession = $this->MgSession->getAdapter()->findOne(array('sid' => $decode->sessionID));

            if (!$mongoSession) {
                if (sourceApp) {
                    header("HTTP/1.0 401 Unauthorized");
                }
                $data['info'] = 'No session data!';
                return $data;
            }

            $sessionData = json_decode($mongoSession->data, true);

            if (isset($mongoSession->expireAt)) {
                $mongoDate = $mongoSession->expireAt->toDateTime();
                $data['sessionExp'] = date('Y-m-d H:i:s', $mongoDate->getTimestamp());
            } elseif ($sessionData['user']['super'] == 1) {
                // Super user case, do nothing specific
            } else {
                $data['loggedOut'] = true;
                return $data;
            }

            $data['orderID'] = $mongoSession->orderID ?? null;
            $data['sessionID'] = $decode->sessionID;
            $data['userEditorID'] = $sessionData['userEditorID'] ?? $decode->userEditorID ?? null;
            $data['service'] = $sessionData['service'] ?? null;
            $data['carts'] = $mongoSession->Carts;

            if (!isset($decode->userID) && (!$sessionData['noLogin'] ?? true)) {
                header("HTTP/1.0 401 Unauthorized");
                $data['info'] = 'Brak identyfikatora użytkownika.';
            } elseif ($sessionData['noLogin'] ?? false) {
                header("HTTP/1.0 401 Unauthorized");
                $data['info'] = 'User not logged.';
                $data['noLogin'] = true;
                $data['token'] = $token;
                return $data;
            }

            $userInfo = $sessionData['user']['ID'] > 0 ? $this->User->get('ID', $sessionData['user']['ID']) : false;
            $data['user'] = array(
                'userID' => $sessionData['user']['ID'] ?? null,
                'onetime' => intval($userInfo['onetime'] ?? 0) === 1,
                'firstname' => $decode->first_name ?? null,
                'lastname' => $decode->last_name ?? null,
                'mail' => $decode->email ?? $decode->login ?? null,
                'super' => $sessionData['user']['super'] ?? null,
            );

            $data[ACCESS_TOKEN_NAME] = $token;
            $data['response'] = true;
            $data['domainID'] = $this->getDomainID();
        } else {
            header("HTTP/1.0 401 Unauthorized");
            $data['info'] = 'Brak tokena';
        }
        return $data;
    }

    public function check() {
        $data = intval(loginType) === 2 ? $this->_secondCheck() : $this->_firstCheck();
        $data['typeOfCheck'] = intval(loginType);
        return $data;
    }

    public function isLogged() {
        return array('response' => $this->_check_login() ? 'true' : 'false');
    }

    public function isAdminEditor() {
        return array('response' => true);
    }
}
