from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NewMP3(models.Model):
    name = models.TextField()
    url = models.TextField( default="http:")
    count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
