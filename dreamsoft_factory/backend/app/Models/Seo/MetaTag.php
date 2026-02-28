<?php

namespace DreamSoft\Models\Seo;

use DreamSoft\Core\Model;

class MetaTag extends Model
{
    /**
     * MetaTag constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('metatags', true);
    }

    /**
     * @param $ID
     * @return bool
     */
    public function getByID($ID)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `ID` = :ID';

        $binds['ID'] = $ID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getAll();

    }

    /**
     * @param $elem
     * @param $elemID
     * @return bool
     */
    public function getByElemID($elem, $elemID)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `' . $elem . '` = :elemID';

        $binds['elemID'] = $elemID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getAll();

    }

    /**
     * Sets the content item in the database.
     * MetaTag.set
     * @param array $item {
     *     Content data to be inserted, with the following structure:
     *
     *     @type int $elemID
     *     @type string $title
     *     @type string $description
     *     @type string $keywords
     *     @type string $lang
     *     @type string|null $og_title The Open Graph title for the content item.
     *     @type string|null $og_url The Open Graph URL associated with the content item.
     *     @type string|null $og_site_name The name of the site for Open Graph metadata.
     *     @type string|null $og_description The Open Graph description.
     *     @type string|null $og_locale The locale code for Open Graph metadata.
     *     @type int|null $imageID ID of the associated image.
     *     @type int|null $og_image_width Width of the Open Graph image in pixels.
     *     @type int|null $og_image_height Height of the Open Graph image in pixels.
     *     @type string|null $og_image_alt Alt text for the Open Graph image.
     *     @type string|null $twitter_card Type of Twitter card to use for the content.
     *     @type string|null $twitter_site Twitter site associated with the content.
     *     @type string|null $twitter_creator Twitter handle of the creator of the content.
     * }
     *
     * @param string $elemID The unique identifier of the element in the database.
     */
    public function set(array $item, string $elem)
    {
        $query = 'INSERT INTO `' . $this->getTableName() . '` 
        (`' . $elem . '`, `title`, `description`, `keywords`, `lang`, 
        `og_title`, `og_url`, `og_site_name`, `og_description`, `og_locale`, `imageID`, 
        `og_image_width`, `og_image_height`, `og_image_alt`, `twitter_card`, `twitter_site`, `twitter_creator`) 
        VALUES (:elemID, :title, :description, :keywords, :lang, 
        :og_title, :og_url, :og_site_name, :og_description, :og_locale, :imageID, 
        :og_image_width, :og_image_height, :og_image_alt, :twitter_card, :twitter_site, :twitter_creator)';

        $binds = [
            'elemID' => $item['elemID'],
            'title' => $item['title'],
            'description' => $item['description'],
            'keywords' => $item['keywords'],
            'lang' => $item['lang'],
            'og_title' => $item['og_title'],
            'og_url' => $item['og_url'],
            'og_site_name' => $item['og_site_name'],
            'og_description' => $item['og_description'],
            'og_locale' => $item['og_locale'],
            'imageID' => $item['imageID'],
            'og_image_width' => $item['og_image_width'],
            'og_image_height' => $item['og_image_height'],
            'og_image_alt' => $item['og_image_alt'],
            'twitter_card' => $item['twitter_card'],
            'twitter_site' => $item['twitter_site'],
            'twitter_creator' => $item['twitter_creator']
        ];

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->lastInsertID();
    }


    /**
     * @param $elem
     * @param $elemID
     * @return bool
     */
    public function removeByElemID($elem, $elemID)
    {

        $query = 'DELETE FROM `' . $this->getTableName() . '` WHERE `' . $elem . '` = :elemID';

        $binds['elemID'] = $elemID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return true;
    }

    /**
     * @param $groupID
     * @return bool|array
     */
    public function getByGroup($groupID)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `groupID` = :groupID AND `typeID` IS NULL';

        $binds['groupID'] = $groupID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getAll();
    }

    /**
     * @param $typeID
     * @return bool
     */
    public function getByType($typeID)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `typeID` = :typeID AND `groupID` IS NULL';

        $binds['typeID'] = $typeID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getAll();
    }

    /**
     * @param $categoryID
     * @return bool
     */
    public function getByCategory($categoryID)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `catID` = :categoryID OR `subcatID` = :categoryID';

        $binds['categoryID'] = $categoryID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getAll();
    }
}