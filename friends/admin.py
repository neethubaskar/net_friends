from django.contrib import admin

from .models import FriendRequest


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_on')
    search_fields = ['from_user', 'to_user']
    list_filter = ['status']

    def from_user(self, obj):
        return obj.created_by

    from_user.short_description = "From User"


admin.site.register(FriendRequest, FriendRequestAdmin)
