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
        r'^(?P<pk>\d+)/$',
        cfg_views.CFGDetail.as_view(),
        name='detail'
    ),
    url(
        r'^(?P<pk>\d+)/create_pda/$',
        cfg_views.ajax_create_pda,
        name='create_pda'
    ),

]