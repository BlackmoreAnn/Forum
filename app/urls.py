from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.QuestionList.as_view(), name='question.list'),
    url(r'^question/(?P<pk>\d+)/$', views.QuestionDetail.as_view(), name='question.detail'),
    url(r'^question/add/$', views.QuestionCreate.as_view(), name='question.create'),
    url(r'^question/(?P<pk>\d+)/update/$', views.QuestionUpdate.as_view(), name='question.update'),
    url(r'^question/(?P<pk>\d+)/delete/$', views.QuestionDelete.as_view(), name='question.delete'),
    url(r'^answer/(?P<question_pk>\d+)/add/$', views.AnswerCreate.as_view(), name='answer.create'),
    url(r'^answer/(?P<question_pk>\d+)/(?P<pk>\d+)/update/$', views.AnswerUpdate.as_view(), name='answer.update'),
    url(r'^answer/(?P<question_pk>\d+)/(?P<pk>\d+)/delete/$', views.AnswerDelete.as_view(), name='answer.delete'),
)

