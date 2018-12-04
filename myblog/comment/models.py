import threading
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class SendEmail(threading.Thread):
    def __init__(self, title, email, comment_content, blog_url):
        self.title = title
        self.email = email
        self.comment_content = comment_content
        self.blog_url = blog_url
        super().__init__()

    def run(self):
        text_content = '评论或回复内容'
        subject, from_email, to = self.title, settings.FROM_EMAIL, self.email
        html_content = render_to_string('comment/send_mail.html',
                                        {'comment_text': self.comment_content, 'url': self.blog_url})
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    # 两个外键关联同一个表时，通过related_name来解决冲突
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name='replies', on_delete=models.CASCADE, null=True)

    def send_email(self):

        # 评论之后发送邮件通知
        if self.parent is None:
            # 评论博客
            email = self.content_object.get_email()
            title = '有人评论你的博客'
        else:
            # 回复评论
            email = self.reply_to.email  # 被回复的人的邮箱
            title = '有人回复你的博客'

        if email != '':
            comment_content = self.text
            blog_url = self.content_object.get_url()
            send__email = SendEmail(title, email, comment_content, blog_url)
            send__email.start()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
