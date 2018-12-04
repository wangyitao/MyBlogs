from django.http import JsonResponse

from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm


def update_commit(requests):
    comment_form = CommentForm(requests.POST, user=requests.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        # 发送邮件通知
        comment.send_email()
        # 返回数据
        data = {
            'status': 'SUCCESS',
            'username': comment.user.get_nickname_or_username(),
            'comment_time': comment.comment_time.timestamp(),  # 返回时间戳
            'text': comment.text.strip(),
            'reply_to': comment.reply_to.get_nickname_or_username() if parent is not None else '',
            'pk': comment.pk,
            'root_pk': comment.root.pk if comment.root is not None else '',
            'content_type': ContentType.objects.get_for_model(comment).model,
        }

    else:
        data = {
            'status': 'ERROR',
            'message': list(comment_form.errors.values())[0][0],
        }
    return JsonResponse(data)
