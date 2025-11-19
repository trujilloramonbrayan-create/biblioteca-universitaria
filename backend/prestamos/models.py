from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from recursos.models import Recurso
from usuarios.models import PerfilUsuario

class Prestamo(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
        ('renovado', 'Renovado'),
    ]
    
    usuario = models.ForeignKey(
    PerfilUsuario, 
    on_delete=models.CASCADE, 
    related_name='prestamos'
    )
    
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, related_name='prestamos')
    
    # Fechas
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion_real = models.DateField(null=True, blank=True)
    
    # Control
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    renovaciones = models.IntegerField(default=0)
    max_renovaciones = models.IntegerField(default=2)
    
    # Observaciones
    notas = models.TextField(blank=True)
    bibliotecario_entrega = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='prestamos_gestionados_entrega'
    )
    bibliotecario_devolucion = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='prestamos_gestionados_devolucion'
    )
    
    def dias_retraso(self):
        """Calcula los días de retraso"""
        if self.estado == 'devuelto' and self.fecha_devolucion_real:
            delta = self.fecha_devolucion_real - self.fecha_devolucion_esperada
            return max(0, delta.days)
        elif self.estado in ['activo', 'vencido']:
            delta = timezone.now().date() - self.fecha_devolucion_esperada
            return max(0, delta.days)
        return 0
    
    def puede_renovar(self):
        """Verifica si el préstamo puede renovarse"""
        return (
            self.estado == 'activo' and 
            self.renovaciones < self.max_renovaciones and
            self.dias_retraso() == 0
        )
    
    def renovar(self, dias=7):
        """Renueva el préstamo"""
        if self.puede_renovar():
            self.fecha_devolucion_esperada += timedelta(days=dias)
            self.renovaciones += 1
            self.save()
            return True
        return False
    
    def __str__(self):
        return f"{self.usuario.username} - {self.recurso.titulo} ({self.estado})"
    
    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ['-fecha_prestamo']


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
        ('expirada', 'Expirada'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()
    fecha_retiro = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True)
    
    def esta_vigente(self):
        """Verifica si la reserva sigue vigente"""
        return self.estado == 'pendiente' and timezone.now() < self.fecha_expiracion
    
    def __str__(self):
        return f"{self.usuario.username} - {self.recurso.titulo} ({self.estado})"
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_reserva']


class Sancion(models.Model):
    TIPO_CHOICES = [
        ('retraso', 'Retraso en devolución'),
        ('dano', 'Daño al material'),
        ('perdida', 'Pérdida del material'),
        ('mal_uso', 'Mal uso de la biblioteca'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sanciones')
    prestamo = models.ForeignKey(Prestamo, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateField()
    dias_sancion = models.IntegerField()
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pagada = models.BooleanField(default=False)
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Sanción {self.get_tipo_display()} - {self.usuario.username}"
    
    class Meta:
        verbose_name = "Sanción"
        verbose_name_plural = "Sanciones"
        ordering = ['-fecha_inicio']