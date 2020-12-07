from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	first_name = models.CharField(max_length=10, default="name")
	second_name = models.CharField(max_length=20, default="username")
	user_image = models.ImageField(default='Unknown_person.jpg', upload_to="media")

	
	def __str__(self):
		return self.first_name + self.second_name

