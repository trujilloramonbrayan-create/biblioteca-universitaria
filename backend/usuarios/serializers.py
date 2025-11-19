from rest_framework import serializers
from .models import PerfilUsuario

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='usuario.first_name', read_only=True)
    apellido = serializers.CharField(source='usuario.last_name', read_only=True)
    email = serializers.EmailField(source='usuario.email', read_only=True)
    username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = PerfilUsuario
        fields = [
            'id',
            'usuario',           # ID del User
            'rol',
            'codigo_universitario',
            'programa_academico',
            'telefono',
            'direccion',
            'fecha_registro',
            'activo',
            'prestamos_permitidos',
            'sancionado',
            'fecha_fin_sancion',
            'motivo_sancion',

            # Campos añadidos del User
            'nombre',
            'apellido',
            'email',
            'username',
        ]
