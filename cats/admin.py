from django.contrib import admin

from .models import Owner, Cat, Achievement, AchievementCat


class AchievementCatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'achievement', 'cat')
    empty_value_display = '-пусто-'


class AchievementAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name')
    search_fields = ('first_name',)
    list_filter = ('first_name',)
    empty_value_display = '-пусто-'


class CatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'birth_year', 'owner')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Owner, OwnerAdmin)
admin.site.register(Cat, CatAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(AchievementCat, AchievementCatAdmin)
