<?php


use Phinx\Migration\AbstractMigration;

class CleanDb extends AbstractMigration
{

    public function up()
    {
        $this->query('drop table if exists advertise, allegro, allegrodeals, allegrosessions, allegrosettings,
    allegrousermail,blog, blogfiles,  bonuscoupons, businessproduct_files, businessproduct_tooltips,
    contents,     coupons, customproduct_files, discounts, discount_groups, documentsdata,
    domains, groups, icons, inpost_status, invoices, letters7post, lettersapaczka, letterskex,
    fotoliacategories, fotoliafavourites, fotoliafilters, fotoliatreecategories,logs,
    mail_contents,mail_footer,mail_module,mailcreations,mailsender,`name-daypl`, newsletter,notloggedphotos,
    opg_config_friendlylinks,  partners, paymentmail, paymentmailrecipments, photocalendar_friendlylinks,
    poczta_envelope, poczta_status, preflight_queue, products, products_order, project, project_categories,
    promotions, promotions_products, realizationtime, realizationtimecontents, realizationtimedetails,
    reclamation, reclamation_files, reclamationaddress, reclamationmessages, reclamationstatuses,
    refconf, refprizes, refusers, settings, specialcalendar_friendlylinks,
    sp_config_attributes,sp_config_options,sp_options_items,sp_products_groups,sp_products_items,
    sp_products_options,sp_products_types,sp_types_attributes, static_prices,staticcontents,statuses, thumbs,
    tmpimages, transactions, turbosms, ups_status, userphotos, users_data_changes, users_rodo_confirms,
    users_rodo_contents, users_rodo_data;');
    }

}
