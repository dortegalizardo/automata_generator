from django.conf.urls import url, include

from cfg import views as cfg_views

app_name = 'cfg_app'

urlpatterns = [
    url(
        r'^$',
        cfg_views.HomeCFG.as_view(),
        name='home'
    ),
    url(
        r'^cfg/(?P<pk>\d+)/$',
        cfg_views.CFGDetail.as_view(),
        name='detail'
    ),

]