
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>",views.profile,name="profile"),
    path("like",views.like,name="like"),
    path("follow/<int:user_profile_id>",views.follow,name="follow"),
    path("sendmessage/<int:user_profile_id>",views.sendit,name="sendit"),
    path("postedit",views.postedit,name="postedit"),
    path("inbox",views.inbox,name="inbox"),
    path("notifications",views.notifications,name="notifications"),
    path("loadbox",views.loadbox,name="loadbox"),
    path("delete/<int:post_id>",views.delete,name="delete"),
    path("load/<int:message_id>",views.load_message,name="load_message"),
    path("directmessages",views.directmessages,name="directmessages")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
    