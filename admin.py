from pfam_maps.models import PfamMaps
from django.contrib import admin



class PfamMapsAdmin(admin.ModelAdmin):
        #fields = ['activity_id', 'conflict_flag', 'domain_name']
        list_display = ('activity_id', 'domain_name', 'category_flag', 'status_flag', 'manual_flag', 'compd_id')
admin.site.register(PfamMaps, PfamMapsAdmin)
