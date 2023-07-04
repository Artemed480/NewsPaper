from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'post_data_time')
    list_filter = ('post_data_time', 'autor', 'post_categories')
    search_fields = ('post_title', 'post_categories', 'autor')


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('category_name', 'subscribers')
    search_fields = ('category_name', 'subscribers')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

