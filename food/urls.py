

from django.urls import path,re_path
from .views import *
urlpatterns = [
    path('index/', index_view,name='index'),
    path('create/', create_view,name='create'),
    re_path(r'^(?P<slug>[\w-]+)/$',detail_view,name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/update/$',update_view,name='update'),
]