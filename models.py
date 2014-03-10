# This was a auto-generated Django model module.
# After generating it with python manage.py inspectdb > pfam_maps/models.py

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
    submitter = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = 'pfam_maps'

class ValidDomains(models.Model):
    entry_id = models.IntegerField(primary_key=True)
    domain_name = models.CharField(max_length=300, blank=True)
    removed_flag = models.IntegerField(null=True, blank=True)
    evidence = models.CharField(max_length=450, blank=True)
    timestamp = models.CharField(max_length=75, blank=True)
    submitter = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = 'valid_domains'


