# from django.db import models


# class CategoryGenreBase(models.Model):
#     name = models.CharField(max_length=256)
#     slug = models.SlugField(unique=True, max_length=50)

#     class Meta:
#         abstract = True
#         ordering = ('name',)

#     def __str__(self):
#         return self.name[:20]


# class Category(CategoryGenreBase):
#     class Meta(CategoryGenreBase.Meta):
#         verbose_name = 'Категория'
#         verbose_name_plural = 'Категории'


# class Genre(CategoryGenreBase):
#     class Meta(CategoryGenreBase.Meta):
#         verbose_name = 'Жанр'
#         verbose_name_plural = 'Жанры'


# class Title(models.Model):
#     name = models.TextField()
#     year = models.PositiveSmallIntegerField()
#     description = models.TextField(blank=True)
#     genre = models.ManyToManyField(
#         Genre,
#         through='GenreTitle',
#         blank=True,
#         related_name='titles',
#     )
#     category = models.ForeignKey(
#         Category,
#         models.SET_NULL,
#         blank=True,
#         null=True,
#         related_name='titles',
#     )

#     class Meta:
#         ordering = ('name',)
#         verbose_name = 'Произведение'
#         verbose_name_plural = 'Произведения'

#     def __str__(self):
#         return self.name[:20]
