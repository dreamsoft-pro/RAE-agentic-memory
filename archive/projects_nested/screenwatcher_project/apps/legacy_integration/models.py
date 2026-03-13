from django.db import models

class ConnectionProfile(models.Model):
    name = models.CharField(max_length=100, unique=True)
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=3306)
    database = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=255, blank=True)
    
    # Priority: If True, settings from Edge client will be ignored
    use_central_config = models.BooleanField(default=False, help_text="If True, Edge client cannot override these settings.")

    class Meta:
        verbose_name = 'External Connection Profile'

    def __str__(self):
        return self.name

class Jobsdata(models.Model):

    jdnr = models.CharField(max_length=64, primary_key=True, db_column='jdnr')
    jdline = models.CharField(max_length=64, blank=True, null=True, db_column='jdline')
    qtyordered = models.IntegerField(blank=True, null=True, db_column='qtyordered')
    linedesc = models.CharField(max_length=255, blank=True, null=True, db_column='linedesc')
    jobformat = models.CharField(max_length=64, blank=True, null=True, db_column='jobformat')
    customer = models.CharField(max_length=255, blank=True, null=True, db_column='customer')
    printformat = models.CharField(max_length=64, blank=True, null=True, db_column='printformat')

    class Meta:
        managed = False
        db_table = 'Jobsdata'
        verbose_name = 'Legacy Job Data'
        verbose_name_plural = 'Legacy Jobs Data'

    def __str__(self):
        return f"{self.jdnr} - {self.customer}"

class Printtemp(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    jdnr = models.CharField(max_length=64, db_column='jdnr')
    jdline = models.CharField(max_length=64, blank=True, null=True, db_column='jdline')
    tiles = models.CharField(max_length=255, blank=True, null=True, db_column='tiles')
    tilecounter = models.IntegerField(blank=True, null=True, db_column='tilecounter')
    qtyprint = models.IntegerField(blank=True, null=True, db_column='qtyprint')
    dtime = models.DateTimeField(blank=True, null=True, db_column='dtime')
    timeprinted = models.CharField(max_length=64, blank=True, null=True, db_column='timeprinted')
    printer = models.CharField(max_length=64, blank=True, null=True, db_column='printer')
    machine = models.CharField(max_length=64, blank=True, null=True, db_column='machine')
    profile = models.CharField(max_length=64, blank=True, null=True, db_column='profile')
    format = models.CharField(max_length=64, blank=True, null=True, db_column='format')
    isprinted = models.BooleanField(default=False, db_column='isprinted')
    bcodeprinted = models.CharField(max_length=255, blank=True, null=True, db_column='bcodeprinted')

    class Meta:
        managed = False
        db_table = 'Printtemp'
        verbose_name = 'Legacy Print Temp'
        verbose_name_plural = 'Legacy Print Temp Entries'

    def __str__(self):
        return f"Entry {self.id} for {self.jdnr}"
