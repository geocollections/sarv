from django.conf.urls import patterns
from apps.acl import admin as acladmin
import os
acl = acladmin.AclAdmin()

urlpatterns = patterns("",
    (r"^$", acl.index),
    (r"^static/(?P<path>.*)$", "django.views.static.serve", {"document_root": os.path.join(os.path.dirname(__file__), "static/acl") }),
    (r"^(?P<action>\w+)/$", acl.router)
)
