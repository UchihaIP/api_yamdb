from django.contrib import admin

from .models import Title, Genre, Category



class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'category',)
    search_fields = ('name',)
    list_filter = ('category', 'genre')
    empty_value_display = '-пусто-'


# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('title_id', 'text', 'score', 'title')


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre) 
admin.site.register(Category)
# admin.site.register(Review, ReviewAdmin) 