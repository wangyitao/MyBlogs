from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm
import re
import copy


def update_commit(requests):
    comment_form = CommentForm(requests.POST, user=requests.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        # 返回数据
        data = {
            'status': 'SUCCESS',
            'username': comment.user.username,
            'comment_time': comment.comment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'text': comment.text.strip(),
        }
    else:
        data = {
            'status': 'ERROR',
            'message': list(comment_form.errors.values())[0][0],
        }
    return JsonResponse(data)
