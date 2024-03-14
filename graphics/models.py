from django.db import models
from users.models import User


class NodeGroups(models.Model):
    title = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,
                              choices=[
                                    ("Yangi", "Yangi"),
                                    ("Faol", "Faol"),
                                    ("Nofaol", "Nofaol"),
                                    ('Arxiv', 'Arxiv')],
                              blank=True
                              )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Script(models.Model):
    question = models.TextField(verbose_name='Savol')
    answer = models.TextField(verbose_name='Javob')
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='child_nodes')
    folder_id = models.ForeignKey(NodeGroups, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.answer

