from django.contrib import admin
from .models import Genre, Title, Category, Review, Comment

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Title, AuthorAdmin)
admin.site.register(Genre, AuthorAdmin)
admin.site.register(Category, AuthorAdmin)
admin.site.register(Review, AuthorAdmin)
admin.site.register(Comment, AuthorAdmin)