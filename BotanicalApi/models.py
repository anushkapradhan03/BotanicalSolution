from django.contrib.auth.models import User
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    detailed_paragraph = models.TextField()
    #image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star_ratings = models.IntegerField()
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
