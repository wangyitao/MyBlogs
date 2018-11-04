from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog


# Create your views here.

# 博客列表
def blog_list(requests):
    context = {
        'blogs': Blog.objects.all()
    }
    return render_to_response('blog_list.html', context)

# 博客详情
def blog_detail(requests, blog_pk):
    context = {
        'blog': get_object_or_404(Blog, pk=blog_pk)
    }

    return render_to_response('blog_detail.html', context)
