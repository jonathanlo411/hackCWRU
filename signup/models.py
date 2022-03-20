from django.db import models

class userprofile(models.Model):
    # User Information
    did = models.CharField(max_length=100, default="error")
    username = models.CharField(max_length=30, default="error")
    access_token = models.CharField(max_length=100, default="error")
    refresh_token = models.CharField(max_length=100, default="error")


    def __str__(self):
        return self.username