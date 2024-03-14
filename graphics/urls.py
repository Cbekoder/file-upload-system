from django.urls import path
from .views import *

urlpatterns = [
    path('groups/', NodeGroupView.as_view(), name='folders'),
    path('groups/<int:pk>', TreeNode.as_view()),
    path('json_form/<int:pk>', JSONConvView.as_view()),
    path('defaultAdd/<int:pk>', DefaultAdd.as_view()),
    path('delgroup/<int:pk>', delete_group),
    path('delscript/<int:pk>', delete_script),
]