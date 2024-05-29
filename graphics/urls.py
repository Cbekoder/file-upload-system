from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="homepage"),
    path('files/<str:type>/<str:category>/', FilesView.as_view(), name='files'),
    path('upload_file/', UploadFileView.as_view(), name='upload_file'),
    # path('groups/<int:pk>', TreeNode.as_view()),
    # path('json_form/<int:pk>', JSONConvView.as_view()),
    # path('defaultAdd/<int:pk>', DefaultAdd.as_view()),
    # path('delgroup/<int:pk>', delete_group),
    # path('delscript/<int:pk>', delete_script),
]