from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator


# Create your views here.

# 博客列表
def blog_list(requests):
    # 分页
    blogs_all_list = Blog.objects.all()  # 获取全部博客
    paginator = Paginator(blogs_all_list, 10)  # 第一个参数是全部内容，第二个是每页多少
    page_num = requests.GET.get('page', 1)  # 获取url的页面参数（get请求）
    page_of_blogs = paginator.get_page(page_num)  # 从分页器中获取指定页码的内容

    context = {
        'page_of_blogs': page_of_blogs,
        'blog_types': BlogType.objects.all(),
    }
    return render_to_response('blog/blog_list.html', context)


# 博客详情
def blog_detail(requests, blog_pk):
    context = {
        'blog': get_object_or_404(Blog, pk=blog_pk)
    }

    return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(requests, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context = {
        'blogs': Blog.objects.filter(blog_type=blog_type),
        'blog_type': blog_type,
        'blog_types': BlogType.objects.all(),
    }
    return render_to_response('blog/blog_with_type.html', context)
