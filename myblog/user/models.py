from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nikename = models.CharField(max_length=20, verbose_name='昵称',default='')

    def __str__(self):
        return '<Profile: {} for {}>'.format(self.nikename, self.user.username)
