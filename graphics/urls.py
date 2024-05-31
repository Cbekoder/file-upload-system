from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="homepage"),
    path('files/<str:typef>/<str:category>/', FilesView.as_view(), name='files'),
    path('upload_file/', UploadFileView.as_view(), name='upload_file'),
    path('file/detail/<int:pk>', FileDetailView.as_view(), name='file_detail'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('roles/', RolesView.as_view(), name='roles'),
    path('download/', download_files)
    # path('groups/<int:pk>', TreeNode.as_view()),
    # path('json_form/<int:pk>', JSONConvView.as_view()),
    # path('defaultAdd/<int:pk>', DefaultAdd.as_view()),
    # path('delgroup/<int:pk>', delete_group),
    # path('delscript/<int:pk>', delete_script),
]