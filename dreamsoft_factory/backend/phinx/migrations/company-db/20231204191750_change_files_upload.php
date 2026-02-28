<?php


use Phinx\Migration\AbstractMigration;

class ChangeFilesUpload extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_config_options add column fileUploadAvailable smallint not null default 0');
        $this->query('alter table ps_user_calc_product_attributes add column fileUploadAvailable smallint null');
        $this->query('alter table ps_user_calc_products add column slope float not null');
        $this->query('alter table dp_products add column sendToFix smallint null default 0');
        $this->query("create table ps_user_calc_product_files
        (
            ID        int primary key,
            userCalcProductAttrOptionID int                  not null,
            modelExtensionID int not null,
            name      varchar(400)         not null,
            accept    tinyint    default 0 not null,
            acceptChangeDate     datetime      null,
            acceptRejectUserID   int           null,
            acceptRejectUserName char(30)      null,
            isLocal   tinyint(1) default 0 not null,
            created   datetime             not null,
            size int null comment 'size in bytes',
            pagesCount int null,
            width decimal(10,2) not null,
            widthNet decimal(10,2) null,
            height decimal(10,2) not null,
            heightNet decimal(10,2) null,
            colorSpace char(11) null,
            dimensionsValid int null,
            backSideTarget int not null default 0,
            fileFixed int not null default 0,
            foreign key (modelExtensionID) references dp_modelsIconsExtensions(ID)
        )");

        $productFiles = $this->fetchAll('select pf.*,cp.ID cpID from dp_productFiles pf 
            join dp_products p on p.ID = pf.productID
            join ps_user_calc_products cp on cp.calcID=p.calcID');

        $id = 0;

        foreach ($productFiles as $fileData) {

            $nameExt = preg_split('/\./', $fileData['name']);
            $stm = $this->query('select ID from dp_modelsIconsExtensions where extension=?', [array_pop($nameExt)]);
            $meIds = $stm->fetchAll();
            $modelExtensionID = $meIds[0]['ID'];

            $stm = $this->query('select * from ps_user_calc_products cp join
                    ps_user_calc_product_attributes pa on cp.ID=pa.calcProductID
                    where pa.calcProductID=? AND pa.attrID=?', [$fileData['cpID'], 1]);

            $attributes = $stm->fetchAll();
            if (!count($attributes) || !$attributes[0]['ID']) {
                continue;
            }
            if(empty($modelExtensionID)){
                continue;
            }
            $this->query('INSERT INTO ps_user_calc_product_files 
                        (ID, userCalcProductAttrOptionID, modelExtensionID, name, accept, isLocal, created, width, height, size) 
                        VALUES (?,?,?,?,?,?,?,?,?,?)', [
                ++$id,
                $attributes[0]['ID'],
                $modelExtensionID,
                $fileData['name'],
                $fileData['accept'],
                $fileData['isLocal'],
                $fileData['created'],
                0, 0, 0]);

        }
        $this->query('update ps_user_calc_product_attributes set fileUploadAvailable=1 where attrID=1');

        $this->query('SET FOREIGN_KEY_CHECKS=0;');

        $this->query("alter table dp_modelsIconsExtensions drop column typeFile, 
                    add column baseExtensionID int not null, 
                    add column `type` enum('pdf','image','bin') not null,
                    add constraint baseExtensionID_fk foreign key(baseExtensionID) references dp_modelsIconsExtensions(ID)");

        $this->query('SET FOREIGN_KEY_CHECKS=1;');

        $types = ['jpg' => 'image', 'tif' => 'image', 'wmf' => 'image', 'pdf' => 'pdf', 'zip' => 'bin'];
        $baseTypes = ['jpeg' => 'jpg', 'tiff' => 'tif'];
        $ext = $this->fetchAll('select * from dp_modelsIconsExtensions');

        foreach ($ext as $e) {
            $isExtension = false;
            foreach ($types as $typeExt => $type) {
                if ($typeExt == $e['extension']) {
                    $isExtension = true;
                    $this->query('update dp_modelsIconsExtensions set baseExtensionID=ID, `type` = ?  where ID=?',
                        [$type, $e['ID']]);
                }
            }
            if (!$isExtension) {
                if (isset($baseTypes[$e['extension']])) {
                    $baseRow = $this->fetchRow('select * from dp_modelsIconsExtensions where extension="' . $baseTypes[$e['extension']] . '"');
                } else {
                    $baseRow = $this->fetchRow('select * from dp_modelsIconsExtensions where extension="zip"');
                }
                $this->query('update dp_modelsIconsExtensions set baseExtensionID=?, `type`=? where ID=?',
                    [$baseRow['ID'], $baseRow['type'], $e['ID']]);
            }
        }
    }

    public function down()
    {
        echo('migration not reversible');
    }
}
