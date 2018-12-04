from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone


# Create your models here.

# 使用到了contenttype 参考网址：https://docs.djangoproject.com/en/2.1/ref/contrib/contenttypes/
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)  # 阅读量
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.read_num)


# 阅读计数扩展方法
class ReadNumExpandMethod:
    def get_read_num(self):  # 获取一对一关联的阅读数
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist as e:
            return 0


class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)  # 日期
    read_num = models.IntegerField(default=0)  # 阅读量
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
