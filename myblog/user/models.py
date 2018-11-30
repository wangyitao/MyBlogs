from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, verbose_name='昵称', default='')

    def __str__(self):
        return '<Profile: {} for {}>'.format(self.nickname, self.user.username)


def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''


def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


def has_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return True if profile.nickname.strip() else False
    return False


User.get_nickname = get_nickname  # 动态绑定方法
User.has_nickname = has_nickname  # 动态绑定方法
User.get_nickname_or_username = get_nickname_or_username  # 动态绑定方法
