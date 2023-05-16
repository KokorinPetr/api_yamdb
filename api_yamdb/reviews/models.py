from django.db import models


class Category(models.Model):
    name = models.CharField('название', max_length=256)
    slug = models.SlugField('ключ', unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('название', max_length=256)
    slug = models.SlugField('ключ', unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField('название произведения', max_length=256)
    year = models.IntegerField('год выпуска')
    description = models.TextField('описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='ключ жанра',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='ключ категории',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name
