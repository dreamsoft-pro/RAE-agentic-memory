<?php


use Phinx\Migration\AbstractMigration;

class RefactorTemplates extends AbstractMigration
{

    public function up()
    {
        $this->query('insert into dp_templates (name,fileName,created, useVariables) values("attribute-filters","attribute-filters", now(),0);');
        $this->query("delete from dp_templates where name in('dla-klientow-faq','dla-klienta-formaty-plikow','dla-klienta-jak-dostarczyc-plik','dla-klienta-jak-przygotowac-plik','dla-klienta-links','technologia-park-maszyn','technologia-postpress','technologia-press','technologia-prepress','technologia-personalizacja','technologia-gadzety','technologia-wielkoformatowy','technologia-cyfrowy','technologia-offset','status-zamowienia','technologia-links','technologia','platnosci','dla-klienta','o-firmie','przygotowanie-plikow');");
    }
    public function down()
    {
        $this->query('delete from dp_templates where name="attribute-filters"');
    }
}

