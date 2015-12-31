from django.conf.urls import patterns, include
import os
import apps.acl.urls as acl_admin
import apps.menu.urls as menu_admin

urlpatterns = patterns("",
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r"^static/(?P<path>.*)$", "django.views.static.serve", {"document_root": os.path.join(os.path.dirname(__file__), "static")}),

    (r"^admin/menu/", include(menu_admin)),
    (r"^admin/acl/", include(acl_admin)),
       
    (r"^loginpsw$", "sarv.views.login_with_password"), #login with username/password
    (r"^login/as$", "sarv.views.index", {"select_user":True}),    
    (r"^login$", "sarv.views.login"),

    (r"^logout$", "sarv.views.logout"),    
    (r"^$", "sarv.views.index"),
) 

from apps.nextify.urls import urlpatterns as nextify_urlpatterns
urlpatterns += nextify_urlpatterns

from apps.custom.urls import urlpatterns as custom_urlpatterns
urlpatterns += custom_urlpatterns

from apps.user_feedback.urls import urlpatterns as user_feedback_urlpatterns
urlpatterns += user_feedback_urlpatterns
