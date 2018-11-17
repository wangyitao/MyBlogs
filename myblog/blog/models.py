from django.db import models
from django.db.models.fields import exceptions
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

# 博客分类
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)  # 博客分类名称

    def __str__(self):  # 显示标签名
        return self.type_name


# 博客
class Blog(models.Model):
    title = models.CharField(max_length=50)  # 博客标题
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)  # 博客分类
    content = RichTextUploadingField()  # 博客内容，使用富文本编辑
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # 博客作者
    created_time = models.DateTimeField(auto_now_add=True)  # 博客创建时间
    last_updated_time = models.DateTimeField(auto_now=True)  # 博客更新事件

    def get_read_num(self):  # 获取一对一关联的阅读数
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist as e:
            return 0

    def __str__(self):  # 显示标题名
        return "<Blog:{}>".format(self.title)

    class Meta:
        ordering = ['-created_time']  # 定义排序规则，按照创建时间倒序


# 阅读量
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)  # 阅读量
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)
