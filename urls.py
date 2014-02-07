from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('pfam_maps.views',
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^evidence/$', 'evidence_portal', name='evidence_portal'),
    url(r'^evidence/(?P<pfam_name>[\w-]+)/$', 'evidence', name='evidence'),
    url(r'^conflicts/$', 'conflicts_portal', name='conflicts_portal'),
    url(r'^resolved/$', 'resolved_portal', name='resolved_portal'),
    url(r'^conflicts/(?P<conflict_id>.+)/$', 'conflicts', name = 'conflicts'),
    url(r'^resolved/(?P<conflict_id>.+)/$', 'resolved', name = 'resolved'),
    url(r'^vote/conflicts/(?P<act>\d+)/(?P<conflict_id>.+)/$', 'vote_on_activity' , name = 'vote_on_activity'),
    url(r'^vote/conflicts/(?P<assay_id>CHEMBL\d+)/(?P<conflict_id>.+)/$', 'vote_on_assay' , name =  'vote_on_assay'),
    url(r'^revoke/resolved/(?P<assay_id>CHEMBL\d+)/(?P<conflict_id>.+)/$', 'revoke_assay' , name  =  'revoke_assay'),
    url(r'^details/conflicts/(?P<act>\d+)/$', 'details', name = 'details'),
    url(r'^accounts/login/$', 'login', name= 'login'),
    )

urlpatterns += patterns('',
            url(r'^admin/', include(admin.site.urls)),
            )

