from django.contrib import admin
from .models import BlogType, Blog, ReadNum


# Register your models here.

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')  # 需要显示的列表


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog_type', 'author', 'get_read_num', 'created_time', 'last_updated_time')


# 上面的装饰器和这句相同
# admin.site.register(Blog,BlogAdmin)u

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('blog', 'read_num')
