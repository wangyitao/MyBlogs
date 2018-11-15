from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.conf import settings

# Create your views here.

# 博客列表
def blog_list(requests):
    # 分页
    blogs_all_list = Blog.objects.all()  # 获取全部博客
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 第一个参数是全部内容，第二个是每页多少
    page_num = requests.GET.get('page', 1)  # 获取url的页面参数（get请求）
    page_of_blogs = paginator.get_page(page_num)  # 从分页器中获取指定页码的内容

    current_page_num = page_of_blogs.number  # 获取当前页
    all_pages = paginator.num_pages
    if all_pages < 5:
        page_range = list(
            range(max(current_page_num - 2, 1),
                  min(all_pages + 1, current_page_num + 3)))  # 获取需要显示的页码 并且剔除不符合条件的页码
    else:
        if current_page_num <= 2:
            page_range = range(1, 5 + 1)
        elif current_page_num >= all_pages - 2:
            page_range = range(all_pages - 4, paginator.num_pages + 1)
        else:
            page_range = list(
                range(max(current_page_num - 2, 1),
                      min(all_pages + 1, current_page_num + 3)))  # 获取需要显示的页码 并且剔除不符合条件的页码

    context = {
        'blogs': page_of_blogs.object_list,
        'page_of_blogs': page_of_blogs,
        'blog_types': BlogType.objects.all(),
        'page_range': page_range,
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
    # 分页
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)  # 获取全部博客
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 第一个参数是全部内容，第二个是每页多少
    page_num = requests.GET.get('page', 1)  # 获取url的页面参数（get请求）
    page_of_blogs = paginator.get_page(page_num)  # 从分页器中获取指定页码的内容

    current_page_num = page_of_blogs.number  # 获取当前页
    all_pages = paginator.num_pages
    if all_pages < 5:
        page_range = list(
            range(max(current_page_num - 2, 1),
                  min(all_pages + 1, current_page_num + 3)))  # 获取需要显示的页码 并且剔除不符合条件的页码
    else:
        if current_page_num <= 2:
            page_range = range(1, 5 + 1)
        elif current_page_num >= all_pages - 2:
            page_range = range(all_pages - 4, paginator.num_pages + 1)
        else:
            page_range = list(
                range(max(current_page_num - 2, 1),
                      min(all_pages + 1, current_page_num + 3)))  # 获取需要显示的页码 并且剔除不符合条件的页码

    context = {
        'blogs': page_of_blogs.object_list,
        'page_of_blogs': page_of_blogs,
        'blog_types': BlogType.objects.all(),
        'page_range': page_range,
        'blog_type': blog_type,
    }

    return render_to_response('blog/blog_with_type.html', context)
