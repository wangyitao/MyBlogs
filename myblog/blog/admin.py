from django.contrib import admin
from .models import BlogType, Blog


# Register your models here.

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')  # 需要显示的列表


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog_type', 'author', 'get_read_num', 'created_time', 'last_updated_time')


