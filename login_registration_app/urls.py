from django.conf.urls import url
from . import views 

print "im in apps urls"

#login_registration_app file
urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^(?P<user_id>\d+)/delete', views.delete)
]