from django.contrib import admin
from .models import Review, Comment


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Review, AuthorAdmin)
admin.site.register(Comment, AuthorAdmin)
