from django.contrib import admin

from .models import User

'''(admin.site.register(
    Category,
    list_display=('name', 'slug'),
    search_fields=('name',),
    list_filter=('name',),
    empty_value_display='-пусто-',
)
admin.site.register(
    Comment,
    list_display=('review', 'text', 'author', 'pub_date'),
    search_fields=('review',),
    list_filter=('review',),
    empty_value_display='-пусто-',
)
admin.site.register(
    Genre,
    list_display=('name', 'slug'),
    search_fields=('name',),
    list_filter=('name',),
    empty_value_display='-пусто-',
)
admin.site.register(
    Review,
    list_display=('title', 'text', 'author', 'score'),
    search_fields=('pub_date',),
    list_filter=('pub_date',),
    empty_value_display='-пусто-',
)
admin.site.register(
    Title,
    list_display=('name', 'year', 'category', 'description'),
    search_fields=('name',),
    list_filter=('name',),
    empty_value_display='-пусто-',
))'''
admin.site.register(
    User,
    list_display=(
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
        'confirmation_code',
    ),
    search_fields=(
        'username',
        'role',
    ),
    list_filter=('username',),
    empty_value_display='-пусто-',
)
