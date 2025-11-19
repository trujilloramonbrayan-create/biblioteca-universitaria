from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class PerfilUsuario(models.Model):
    ROLES = [
        ('estudiante', 'Estudiante'),
        ('docente', 'Docente'),
        ('bibliotecario', 'Bibliotecario'),
        ('administrador', 'Administrador'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    codigo_universitario = models.CharField(
        max_length=20, 
        unique=True,
        validators=[RegexValidator(r'^\d{8,12}$', 'Código debe tener entre 8 y 12 dígitos')]
    )
    programa_academico = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    prestamos_permitidos = models.IntegerField(default=3)  # Máximo de préstamos simultáneos
    
    # Campos para sanciones
    sancionado = models.BooleanField(default=False)
    fecha_fin_sancion = models.DateField(null=True, blank=True)
    motivo_sancion = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"