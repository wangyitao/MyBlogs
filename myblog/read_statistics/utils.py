# -*- coding: utf-8 -*-
# @Time    : 18-11-17 下午10:03
# @Author  : Felix Wang
import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from django.core.cache import cache
from .models import ReadNum, ReadDetail
from blog.models import Blog


def read_statistics_once_read(requests, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '{}_{}_read'.format(ct.model, obj.pk)

    # 获取并处理阅读计数
    if not requests.COOKIES.get(key):
        # 总阅读量+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # 处理阅读量
        readnum.read_num += 1
        readnum.save()

        # 当天阅读量+1
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()

    return key


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):  # 统计7天的阅读量
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))  # 将日期格式转成字符串
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)  # 如果有阅读量则阅读量否则置0
    return dates, read_nums


# 获取某天的阅读量综合
def get_x_days_hot_data(x_days):
    # 如果缓存有值，取缓存的值
    cache_data = cache.get('cache_data_for_{}_days'.format(x_days))
    if cache_data:
        return cache_data

    today = timezone.now().date()
    if x_days == 0:  # 表示今天
        date_blogs = Blog.objects.filter(read_details__date=today)
    else:  # 不等于0表示往前多少天
        date = today - datetime.timedelta(days=x_days)
        date_blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date)

    read_details = date_blogs.values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by(
        '-read_num_sum')[:7]  # 分组，求和

    cache.set('cache_data_for_{}_days'.format(x_days), read_details,
              3600 * 3 if x_days else 1800)  # 设置缓存，三小时更新一次,如果是当日阅读量半小时更新一次
    return read_details
