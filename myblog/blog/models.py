from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNumExpandMethod, ReadDetail


# Create your models here.

# 博客分类
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)  # 博客分类名称

    def __str__(self):  # 显示标签名
        return self.type_name


# 博客
class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)  # 博客标题
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)  # 博客分类
    content = RichTextUploadingField()  # 博客内容，使用富文本编辑
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 博客作者
    read_details = GenericRelation(ReadDetail)  # 关联到阅读表
    created_time = models.DateTimeField(auto_now_add=True)  # 博客创建时间
    last_updated_time = models.DateTimeField(auto_now=True)  # 博客更新事件

    def get_url(self):  # 获取博客的url路径
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):  # 获取博客作者的邮箱
        return self.author.email

    def __str__(self):  # 显示标题名
        return "<Blog:{}>".format(self.title)

    class Meta:
        ordering = ['-created_time']  # 定义排序规则，按照创建时间倒序
