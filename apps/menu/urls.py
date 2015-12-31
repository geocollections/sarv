import os
from django.conf.urls import patterns
from apps.menu import admin

menu = admin.MenuAdmin()

urlpatterns = patterns("",
    (r"^$", menu.indexsimple),
    (r"^static/(?P<path>.*)$", "django.views.static.serve", {"document_root": os.path.join(os.path.dirname(__file__), "static/menu") }),
    (r"^(?P<action>\w+)/$", menu.router),
)
