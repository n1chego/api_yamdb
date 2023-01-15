from django.contrib import admin
from .models import Genre, Title, Category


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Title, AuthorAdmin)
admin.site.register(Genre, AuthorAdmin)
admin.site.register(Category, AuthorAdmin)
