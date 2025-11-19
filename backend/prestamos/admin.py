from django.contrib import admin
from .models import Prestamo, Reserva, Sancion

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'recurso', 'fecha_prestamo', 'fecha_devolucion_esperada', 'estado', 'renovaciones', 'dias_retraso')
    list_filter = ('estado', 'fecha_prestamo')
    search_fields = ('usuario__username', 'recurso__titulo')
    readonly_fields = ('fecha_prestamo', 'dias_retraso')
    
    fieldsets = (
        ('Información del Préstamo', {
            'fields': ('usuario', 'recurso', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_prestamo', 'fecha_devolucion_esperada', 'fecha_devolucion_real')
        }),
        ('Renovaciones', {
            'fields': ('renovaciones', 'max_renovaciones')
        }),
        ('Control', {
            'fields': ('bibliotecario_entrega', 'bibliotecario_devolucion', 'notas')
        }),
    )
    
    actions = ['marcar_devuelto']
    
    def marcar_devuelto(self, request, queryset):
        from django.utils import timezone
        for prestamo in queryset:
            prestamo.estado = 'devuelto'
            prestamo.fecha_devolucion_real = timezone.now().date()
            prestamo.save()
            prestamo.recurso.actualizar_disponibilidad()
        self.message_user(request, f"{queryset.count()} préstamos marcados como devueltos.")
    marcar_devuelto.short_description = "Marcar como devuelto"

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'recurso', 'fecha_reserva', 'fecha_expiracion', 'estado', 'esta_vigente')
    list_filter = ('estado', 'fecha_reserva')
    search_fields = ('usuario__username', 'recurso__titulo')
    readonly_fields = ('fecha_reserva',)

@admin.register(Sancion)
class SancionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'fecha_inicio', 'fecha_fin', 'multa', 'pagada', 'activa')
    list_filter = ('tipo', 'activa', 'pagada')
    search_fields = ('usuario__username', 'descripcion')
    readonly_fields = ('fecha_inicio',)