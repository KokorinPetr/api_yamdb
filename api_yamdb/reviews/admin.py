from django.contrib import admin
from .models import Title, Genre, Comment, Category, GenreTitle, Review

admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Review)
