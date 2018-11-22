# -*- coding: utf-8 -*-
# @Time    : 18-11-22 下午7:48
# @Author  : Felix Wang

from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

# 注册自定义模板标签
register = template.Library()


# 获取评论计数
@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


# 获取评论表单
@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return CommentForm(
        initial={'content_type': content_type.model, 'object_id': obj.pk, 'reply_comment_id': 0})


# 获取评论列表
@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')  # 评论内容
