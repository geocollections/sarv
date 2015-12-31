from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'^test/', 'apps.custom.views.testpage'),
    (r'^doi/', 'apps.custom.views.doi'),
    (r'^relocate_location','apps.custom.views.relocate_location'),
)

