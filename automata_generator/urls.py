from django.conf.urls import url, include

from automata_generator import views as au_views

app_name = 'automata_app'

urlpatterns = [
    url(
        r'^$',
        au_views.HomeAutomata.as_view(),
        name='home'
    ),
    url(
        r'^automata/(?P<pk>\d+)/$',
        au_views.AutomataDetail.as_view(),
        name='detail'
    ),
    url(
        r'^get_states/(?P<pk>\d+)/$',
        au_views.ajax_get_states,
        name='get_states'
    ),
    url(
        r'^get_transitions/(?P<pk>\d+)/$',
        au_views.ajax_get_transitions,
        name='get_transitions'
    ),
    url(
        r'^test_automata/(?P<pk>\d+)/$',
        au_views.ajax_test_automata,
        name='test_automata'
    )

]

