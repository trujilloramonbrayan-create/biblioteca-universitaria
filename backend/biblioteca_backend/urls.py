from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('prestamos.urls')),
    path('api/', include('usuarios.urls')),
    #path('api/', include('notificaciones.urls')),
    path('api/', include('recursos.urls')), 
]