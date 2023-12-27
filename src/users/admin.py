from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin
from django.contrib.auth.models import Group
from .models import CustomGroup, CustomPermission
from django.utils.translation import gettext_lazy as _


admin.site.site_header = "Administração"
admin.site.index_title = ""

admin.site.unregister(Group)

@admin.register(CustomGroup)
class CustomGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomPermission)
class CustomPermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(get_user_model())
class UserAdmin(auth_admin.UserAdmin):
    model = get_user_model()
    list_display = ('email',)
    ordering = ('email', )
    list_filter = ()
    search_fields = ()
    readonly_fields = ('is_superuser', 'last_login', 'id')
    add_fieldsets = (
        (_('Login data'), {
                'fields': ('email', 'password1', 'password2')
        }),

        (_('Permission'), {
            'fields': ('is_superuser', 'groups', 'user_permissions')
        }),
    )
    fieldsets = (        
        (_('Identification'), {
            'fields': ('id',),
        }),

        (_('Login data'), {
            'fields': ('email', 'password', 'last_login')
        }),

        (_('Permission'), {
            'fields': ('is_superuser', 'groups', 'user_permissions')
        }),
    )

