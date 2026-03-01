<?php

namespace DreamSoft\Libs;
class Data {
    
    public $post = array();
    
    public function __construct() {
        $post = NULL;
        if( $_SERVER["REQUEST_METHOD"] == "POST" && isset($_SERVER["CONTENT_TYPE"]) && stripos($_SERVER["CONTENT_TYPE"], "application/json") === 0) {
            $post = json_decode(file_get_contents("php://input"), true);
        } elseif( !empty($_POST) ){
            $post = $_POST;
        }
        $this->post = $post;
    }

    /**
     * @param $key string|array
     * @param $dataType null|string [bool]
     * @return mixed|null
     */
    public function getPost($key, $dataType = null)
    {
        $result = null;
        if (!is_array($key)) {
            if (isset($this->post[$key])) {
                $result = $this->post[$key];
                if ($dataType && $dataType == 'bool') {
                    $result = isset($result) ? 1 : 0;
                }
            } else if ($dataType == 'bool') {
                $result = 0;
            }
        } else {
            $result = [];
            foreach ($key as $k) {
                $result[$k] = isset($this->post[$k]) ? $this->post[$k] : null;
            }
        }
        return $result;
    }
    
    public function getAllPost() {
        return $this->post;
    }
    
}
