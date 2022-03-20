from django.db import models

class userprofile(models.Model):
    # User Information
    username = models.CharField(max_length=30, default="error")
    password = models.CharField(max_length=50, default="error")
    access_token = models.CharField(max_length=100, default="error")
    refresh_token = models.CharField(max_length=100, default="error")
    did = models.CharField(max_length=100, default="error")
    duser = models.CharField(max_length=100, default="error")
    

    def __str__(self):
        return self.username

    def add(self, acc, ref, dsid, dsuser):
        self.access_token = acc
        self.refresh_token = ref
        self.did = dsid
        self.duser = dsuser