from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read
from .models import Blog, BlogType


# 分页部分公共代码
def blog_list_common_data(requests, blogs_all_list):
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

    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict = {
            blog_date: blog_count
        }

    return {
        'blogs': page_of_blogs.object_list,
        'page_of_blogs': page_of_blogs,
        'blog_types': BlogType.objects.annotate(blog_count=Count('blog')),  # 添加查询并添加字段
        'page_range': page_range,
        'blog_dates': blog_dates_dict
    }


# 博客列表
def blog_list(requests):
    blogs_all_list = Blog.objects.all()  # 获取全部博客
    context = blog_list_common_data(requests, blogs_all_list)
    return render(requests, 'blog/blog_list.html', context)


# 根据类型筛选
def blogs_with_type(requests, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)  # 获取全部博客
    context = blog_list_common_data(requests, blogs_all_list)
    context['blog_type'] = blog_type
    return render(requests, 'blog/blog_with_type.html', context)


# 根据日期筛选
def blogs_with_date(requests, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)  # 获取全部博客
    context = blog_list_common_data(requests, blogs_all_list)
    context['blogs_with_date'] = '{}年{}日'.format(year, month)
    return render(requests, 'blog/blog_with_date.html', context)


# 博客详情
def blog_detail(requests, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    obj_key = read_statistics_once_read(requests, blog)

    context = {
        'blog': blog,
        'previous_blog': Blog.objects.filter(created_time__gt=blog.created_time).last(),
        'next_blog': Blog.objects.filter(created_time__lt=blog.created_time).first(),
    }
    response = render(requests, 'blog/blog_detail.html', context)
    response.set_cookie(obj_key, 'true')

    return response
