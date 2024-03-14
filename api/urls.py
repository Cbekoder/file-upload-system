from rest_framework import routers
from django.urls import path, include
from .views import *


urlpatterns = [
    path('script/', ScriptTreeView.as_view(), name='script_tree_view'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]