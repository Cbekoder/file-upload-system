from django.db import models
from users.models import User
class Numbers(models.Model):
    number = models.CharField(max_length=13)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

class Calls(models.Model):
    # user=models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.ForeignKey(Numbers, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=15, default="initial")

    def __str__(self):
        return self.number







