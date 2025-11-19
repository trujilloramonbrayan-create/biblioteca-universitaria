from django.urls import path
from . import views

urlpatterns = [
    path('prestamos/', views.listar_prestamos),
    path('prestamos/crear/', views.crear_prestamo),
    path('prestamos/<int:pk>/actualizar/', views.actualizar_prestamo),
    path('prestamos/<int:pk>/eliminar/', views.eliminar_prestamo),
]
