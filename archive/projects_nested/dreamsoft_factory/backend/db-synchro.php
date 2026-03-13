<?php

try {
    $db = new PDO('mysql:host=' . getenv('DB_SETTINGS_HOST') . ';dbname=' . getenv('PRINTING_HOUSE_DB_NAME'), getenv('DB_DEVELOPER_USER'), getenv('DB_DEVELOPER_PASSWORD'),
        array(
            PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8"
        )
    );
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $db->query('truncate table dp_cache');

} catch (PDOException $e) {
    error_log($e->getMessage());
}
