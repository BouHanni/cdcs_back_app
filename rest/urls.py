""" URL Configuration
"""
from django.conf.urls import url
from rest import views as mdcs_data_views


urlpatterns = [
	url(r'^data/(?P<pk>\w+)/$', mdcs_data_views.DataList.as_view(),name='mdcs_rest_data_list'),
]