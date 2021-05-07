# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Area(models.Model):
    country_id = models.IntegerField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area'

    def __str__(self):
        return self.cname if self.cname else self.name if self.name else "null"
class Countries(models.Model):
    country_id = models.SmallAutoField(primary_key=True)
    continent_id = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    full_cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'

    def __str__(self):
        return self.cname if self.cname else self.name if self.name else "null"

class States(models.Model):
    state_id = models.SmallAutoField(primary_key=True)
    # country_id = models.SmallIntegerField()
    country_id = models.ForeignKey(Countries, db_column='country_id', null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    code_full = models.CharField(max_length=255, blank=True, null=True)
    area_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'states'

    def __str__(self):
        return self.cname if self.cname else self.name if self.name else "null"

# from smart_selects.db_fields import ChainedForeignKey

class Cities(models.Model):
    city_id = models.SmallAutoField(primary_key=True)
    # state_id = models.SmallIntegerField()
    state_id = models.ForeignKey(States, db_column='state_id', null=True, on_delete=models.SET_NULL)
    # state_id = ChainedForeignKey(States, chained_field='country_id', show_all=False, auto_choose=True, sort=True, db_column='state_id')
    country_id = models.ForeignKey(Countries, db_column='country_id', null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    code_full = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'cities'

    def __str__(self):
        return self.cname if self.cname else self.name if self.name else "null"
class Regions(models.Model):
    id = models.SmallAutoField(primary_key=True)
    city_id = models.SmallIntegerField()
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=50, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    code_full = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'regions'

    def __str__(self):
        return self.cname if self.cname else self.name if self.name else "null"


class Continents(models.Model):
    name = models.CharField(max_length=16, blank=True, null=True)
    cname = models.CharField(max_length=16, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'continents'
    def __str__(self):
        return self.cname if self.cname else self.name if self.name else "null"