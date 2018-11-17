# -*- coding: utf-8 -*-
# @Time    : 18-11-17 下午10:03
# @Author  : Felix Wang
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum


def read_statistics_once_read(requests, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '{}_{}_read'.format(ct.model, obj.pk)

    # 获取并处理阅读计数
    if not requests.COOKIES.get(key):
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        # 处理阅读量
        readnum.read_num += 1
        readnum.save()
    return key
