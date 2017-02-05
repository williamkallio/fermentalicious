from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
     # ex: /brew/5/
    url(r'^(?P<beverage_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /brew/5/results/
    #url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /brew/5/vote/
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
