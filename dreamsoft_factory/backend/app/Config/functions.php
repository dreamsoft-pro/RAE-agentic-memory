<?php

if (!function_exists('http_response_code')) {
    function http_response_code($code = null) {
        static $statusTexts = [
            100 => 'Continue',
            101 => 'Switching Protocols',
            200 => 'OK',
            201 => 'Created',
            202 => 'Accepted',
            203 => 'Non-Authoritative Information',
            204 => 'No Content',
            205 => 'Reset Content',
            206 => 'Partial Content',
            300 => 'Multiple Choices',
            301 => 'Moved Permanently',
            302 => 'Moved Temporarily',
            303 => 'See Other',
            304 => 'Not Modified',
            305 => 'Use Proxy',
            400 => 'Bad Request',
            401 => 'Unauthorized',
            402 => 'Payment Required',
            403 => 'Forbidden',
            404 => 'Not Found',
            405 => 'Method Not Allowed',
            406 => 'Not Acceptable',
            407 => 'Proxy Authentication Required',
            408 => 'Request Time-out',
            409 => 'Conflict',
            410 => 'Gone',
            411 => 'Length Required',
            412 => 'Precondition Failed',
            413 => 'Request Entity Too Large',
            414 => 'Request-URI Too Large',
            415 => 'Unsupported Media Type',
            500 => 'Internal Server Error',
            501 => 'Not Implemented',
            502 => 'Bad Gateway',
            503 => 'Service Unavailable',
            504 => 'Gateway Time-out',
            505 => 'HTTP Version not supported'
        ];

        if ($code !== null) {
            if (!isset($statusTexts[$code])) {
                exit('Unknown http status code "' . htmlentities($code) . '"');
            }

            $protocol = $_SERVER['SERVER_PROTOCOL'] ?? 'HTTP/1.0';
            header("$protocol $code {$statusTexts[$code]}");

            $GLOBALS['http_response_code'] = $code;
        } else {
            $code = $GLOBALS['http_response_code'] ?? 200;
        }

        return $code;
    }
}

if (!function_exists('apache_request_headers')) {
    function apache_request_headers() {
        $headers = [];
        $prefix = '/\AHTTP_/';
        foreach ($_SERVER as $key => $value) {
            if (preg_match($prefix, $key)) {
                $header = preg_replace($prefix, '', $key);
                $header = str_replace('_', ' ', strtolower($header));
                $header = str_replace(' ', '-', ucwords($header));
                $headers[$header] = $value;
            }
        }
        return $headers;
    }
}

if (!function_exists('array_key_first')) {
    function array_key_first(array $array) {
        foreach ($array as $key => $value) {
            return $key;
        }
        return null;
    }
}
