from django.conf.urls import patterns, url
from apps.user_feedback.views import read, add, mark_resolved

urlpatterns = patterns("",
    url(r"^get_user_messages", read),
    url(r"^user_messages_add", add),
    url(r"^user_messages_mark_resolved", mark_resolved)
)
