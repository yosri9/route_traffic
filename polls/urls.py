from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.averageData, name='averagedata'),

]
