# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class PfamMaps(models.Model):
    map_id = models.IntegerField(primary_key=True)
    activity_id = models.IntegerField(null=True, blank=True)
    compd_id = models.IntegerField(null=True, blank=True)
    domain_name = models.CharField(max_length=300, blank=True)
    category_flag = models.IntegerField(null=True, blank=True)
    status_flag = models.IntegerField(null=True, blank=True)
    manual_flag = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=450, blank=True)
    timestamp = models.CharField(max_length=75, blank=True)
    class Meta:
        db_table = 'pfam_maps'

