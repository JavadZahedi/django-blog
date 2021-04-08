from django.contrib import admin
from .models import Category, Article, UserProfile

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'position')


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'jpublish', 'status', 'categories_to_str')

    def categories_to_str(self, obj):
        return ', '.join(cat.name for cat in obj.categories.all())
    categories_to_str.short_description = 'دسته بندی‌ (ها)'


admin.site.register(Article, ArticleAdmin)

admin.site.register(UserProfile)