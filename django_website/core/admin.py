from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    fields = ('id', 'notif_type', 'value', 'model_created_at')
    list_display = ['id', 'notif_type', 'value', 'model_created_at']
    list_display_links = ['id', 'notif_type', 'value', 'model_created_at']
    readonly_fields = ('id', 'notif_type', 'value', 'model_created_at')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, extra_context=extra_context)


@admin.register(MiddlewareFilter)
class MiddlewareFilterAdmin(admin.ModelAdmin):
    fields = ('interval_publish_to_blockchain', 'interval_publish_to_broker', 'model_modified_at')
    list_display = ['name', 'interval_publish_to_blockchain', 'interval_publish_to_broker', 'model_modified_at']
    list_display_links = ['name', 'interval_publish_to_blockchain', 'interval_publish_to_broker', 'model_modified_at']
    readonly_fields = ('name', 'model_modified_at',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, extra_context=extra_context)


admin.site.unregister(Group)
