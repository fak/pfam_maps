from django.conf.urls import patterns, include, url
#from pfam_maps.forms import ExRegistrationForm
#from registration.backends.default.views import RegistrationView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('pfam_maps.views',
    url(r'^$', 'index', name='index'),
    url(r'^logs/portal/$', 'logs_portal', name='logs_portal'),
    url(r'^logs/query/$', 'query_logs', name='query_logs'),
    url(r'^logs/download/$', 'download_logs', name='download_logs'),
    url(r'^logs/$', 'logs', name='logs'),
    url(r'^evidence/$', 'evidence_portal', name='evidence_portal'),
    url(r'^evidence/download/$', 'download_pfam', name='download_pfam'),
    url(r'^evidence/(?P<pfam_name>[\w-]+)/$', 'evidence', name='evidence'),
    url(r'^conflicts/$', 'conflict_portal', name='conflict_portal'),
    url(r'^resolved/$', 'resolved_portal', name='resolved_portal'),
    url(r'^conflicts/(?P<conflict_id>.+)/$', 'conflicts', name = 'conflicts'),
    url(r'^resolved/(?P<conflict_id>.+)/$', 'resolved', name = 'resolved'),
    url(r'^vote/conflicts/(?P<assay_id>CHEMBL\d+)/(?P<conflict_id>.+)/$', 'vote_on_assay' , name =  'vote_on_assay'),
    url(r'^revoke/resolved/(?P<assay_id>CHEMBL\d+)/(?P<conflict_id>.+)/$', 'revoke_assay' , name  =  'revoke_assay'),
    url(r'^accounts/login/$', 'login_view', name= 'login'),
    url(r'^accounts/logout/$', 'logout_view', name= 'logout'),
    url(r'^accounts/profile/$', 'user_portal', name= 'user_portal'),
    url(r'^about/$', 'about', name= 'about'),
    url(r'^accounts/register/$', 'registration_view', name = 'user_registration'),
    )

urlpatterns += patterns('',
            )

