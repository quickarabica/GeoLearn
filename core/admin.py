from django.contrib import admin
from django.contrib.auth.models import User
from .models import BlogPost,event1,event2,contact

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(author=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj is not None and obj.author != request.user:
                return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj is not None and obj.author != request.user:
                return False
        return super().has_delete_permission(request, obj)

admin.site.register(BlogPost, BlogPostAdmin)

admin.site.register(contact)     

admin.site.register(event1)     

admin.site.register(event2)     