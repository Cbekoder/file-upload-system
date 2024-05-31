from django.db import models
from users.models import User, Role
from django.db.models.signals import post_delete
from django.dispatch import receiver

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

    def delete(self, *args, **kwargs):
        self.file.delete()  # Delete the file from the filesystem
        super().delete(*args, **kwargs)  # Call the parent class delete method

# Signal to ensure files are deleted when a File instance is deleted
@receiver(post_delete, sender=File)
def delete_file_on_model_delete(sender, instance, **kwargs):
    instance.file.delete(False)


class RecievedFiles(models.Model):
    file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True, null=True)
    isRead = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.file.description

