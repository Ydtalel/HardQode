from django.contrib import admin
from .models import Product, Lesson, ViewingStatus


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__username')
    list_filter = ('owner',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_seconds')
    list_filter = ('products',)
    filter_horizontal = ('products',)


@admin.register(ViewingStatus)
class ViewingStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'viewed', 'view_time_seconds', 'get_date_viewed')
    list_filter = ('lesson__products', 'viewed')
    search_fields = ('user__username', 'lesson__title')

    def get_date_viewed(self, obj):
        return obj.date_viewed.strftime("%Y-%m-%d %H:%M:%S") if obj.date_viewed else "N/A"

    get_date_viewed.short_description = 'Date Viewed'
