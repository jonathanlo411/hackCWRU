from django.db import models

class userprofile(models.Model):
    # User Information
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username