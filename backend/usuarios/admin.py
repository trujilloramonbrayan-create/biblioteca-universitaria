from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_rol', 'is_staff')
    
    def get_rol(self, obj):
        try:
            return obj.perfil.get_rol_display()
        except:
            return '-'
    get_rol.short_description = 'Rol'

# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'codigo_universitario', 'programa_academico', 'sancionado', 'activo')
    list_filter = ('rol', 'sancionado', 'activo')
    search_fields = ('usuario__username', 'codigo_universitario', 'programa_academico')
    readonly_fields = ('fecha_registro',)