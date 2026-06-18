from django.contrib import admin
from .models import Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'community', 'status', 'claimed_by', 'is_deleted', 'created_at')
    list_filter = ('status', 'is_deleted', 'created_at')
    search_fields = ('title', 'community', 'hashtags')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PostImageInline]

    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'community', 'twitter_link', 'comment_text', 'hashtags')
        }),
        ('Status', {
            'fields': ('status', 'claimed_by', 'is_deleted')
        }),
        ('Meta', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('post__title',)
    readonly_fields = ('uploaded_at',)
