from django.db import models
from users.models import User, Role

class Category(models.Model):
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_done_required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class File(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='files')
    description = models.TextField()
    uploaded_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender')
    to_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='receiver_user')

    def __str__(self):
        return self.description


class RecievedFiles(models.Model):
    file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True, null=True)
    isRead = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)

    def __str__(self):
        return self.file.description

