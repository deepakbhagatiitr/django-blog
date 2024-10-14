from django.contrib import admin
from post.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')  # Shows title, author, and date in admin panel

admin.site.register(Article, ArticleAdmin)
