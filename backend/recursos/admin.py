from django.contrib import admin
from .models import Recurso

@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('codigo_interno', 'titulo', 'autor', 'tipo', 'formato', 'estado', 'copias_disponibles', 'veces_prestado')
    list_filter = ('tipo', 'formato', 'estado', 'categoria')
    search_fields = ('titulo', 'autor', 'isbn', 'codigo_interno', 'palabras_clave')
    list_editable = ('estado',)
    readonly_fields = ('fecha_registro', 'fecha_actualizacion', 'veces_prestado')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'autor', 'tipo', 'formato', 'codigo_interno')
        }),
        ('Publicación', {
            'fields': ('isbn', 'editorial', 'anio_publicacion', 'edicion', 'idioma', 'paginas')
        }),
        ('Clasificación', {
            'fields': ('categoria', 'materia', 'palabras_clave', 'descripcion', 'resumen')
        }),
        ('Disponibilidad', {
            'fields': ('estado', 'numero_copias', 'copias_disponibles', 'ubicacion')
        }),
        ('Recursos Digitales', {
            'fields': ('url_acceso', 'archivo'),
            'classes': ('collapse',)
        }),
        ('Estadísticas', {
            'fields': ('veces_prestado', 'fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )