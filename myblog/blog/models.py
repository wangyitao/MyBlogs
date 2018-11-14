from django.db import models
from django.contrib.auth.models import User


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
    content = models.TextField()  # 博客内容
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # 博客作者
    created_time = models.DateTimeField(auto_now_add=True)  # 博客创建时间
    last_updated_time = models.DateTimeField(auto_now=True)  # 博客更新事件

    def __str__(self):  # 显示标题名
        return "<Blog:{}>".format(self.title)

    class Meta:
        ordering = ['-created_time']  # 定义排序规则，按照创建时间倒序
