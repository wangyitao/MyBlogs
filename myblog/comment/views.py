from django.shortcuts import render, reverse, redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType


def update_commit(requests):
    referer = requests.META.get('HTTP_REFERER', reverse('home'))  # 访问过来的页面
    if not requests.user.is_authenticated:  # 判断用户是否登录
        return render(requests, 'error.html', {'message': '用户未登录', 'redirect_to': referer})

    text = requests.POST.get('text', '').strip()
    if not text:  # 判断内容是否为空
        return render(requests, 'error.html', {'message': '评论内容为空', 'redirect_to': referer})

    try:
        content_type = requests.POST.get('content_type', '')
        object_id = int(requests.POST.get('object_id', ''))
        # 通过反射获取对应的模型
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(requests, 'error.html', {'message': '评论对象不存在', 'redirect_to': referer})

    # 保存评论
    comment = Comment()
    comment.user = requests.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()

    return redirect(referer)
