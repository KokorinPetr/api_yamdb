from django.contrib import admin

from titles.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('slug',)
    empty_value_display = '-пусто-'
