from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator

class Recurso(models.Model):
    TIPO_CHOICES = [
        ('libro', 'Libro'),
        ('revista', 'Revista'),
        ('articulo', 'Artículo'),
        ('tesis', 'Tesis'),
        ('ebook', 'Libro Digital'),
        ('revista_digital', 'Revista Digital'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    ]
    
    FORMATO_CHOICES = [
        ('fisico', 'Físico'),
        ('digital', 'Digital'),
    ]
    
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('reservado', 'Reservado'),
        ('mantenimiento', 'Mantenimiento'),
        ('extraviado', 'Extraviado'),
        ('baja', 'Dado de Baja'),
    ]
    
    # Información básica
    titulo = models.CharField(max_length=300)
    autor = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    formato = models.CharField(max_length=10, choices=FORMATO_CHOICES, default='fisico')
    
    # Identificación
    isbn = models.CharField(max_length=17, unique=True, blank=True, null=True, help_text="ISBN-10 o ISBN-13")
    codigo_interno = models.CharField(max_length=20, unique=True)
    
    # Publicación
    editorial = models.CharField(max_length=150, blank=True)
    anio_publicacion = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(2100)]
    )
    edicion = models.CharField(max_length=50, blank=True)
    idioma = models.CharField(max_length=50, default='Español')
    
    # Clasificación
    categoria = models.CharField(max_length=100)
    palabras_clave = models.CharField(max_length=300, blank=True, help_text="Separadas por comas")
    materia = models.CharField(max_length=100, blank=True)
    
    # Ubicación física
    ubicacion = models.CharField(max_length=50, blank=True, help_text="Ej: Estante A3, Nivel 2")
    numero_copias = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    copias_disponibles = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    
    # Recursos digitales
    url_acceso = models.URLField(blank=True, null=True, validators=[URLValidator()])
    archivo = models.FileField(upload_to='recursos_digitales/', blank=True, null=True)
    
    # Información adicional
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    descripcion = models.TextField(blank=True)
    resumen = models.TextField(blank=True)
    paginas = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    
    # Control
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    veces_prestado = models.IntegerField(default=0)  # Para reportes
    
    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.formato})"
    
    def actualizar_disponibilidad(self):
        """Actualiza las copias disponibles"""
        from prestamos.models import Prestamo
        prestamos_activos = Prestamo.objects.filter(
            recurso=self,
            estado='activo'
        ).count()
        self.copias_disponibles = max(0, self.numero_copias - prestamos_activos)
        self.save()
    
    class Meta:
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"
        ordering = ['-fecha_registro']