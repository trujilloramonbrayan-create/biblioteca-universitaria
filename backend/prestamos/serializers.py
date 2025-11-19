from rest_framework import serializers
from .models import Prestamo
from usuarios.models import PerfilUsuario
from usuarios.serializers import PerfilUsuarioSerializer
from recursos.models import Recurso
from recursos.serializers import RecursoSerializer


class PrestamoSerializer(serializers.ModelSerializer):
    # ====== LECTURA (lo que ve Angular) ======
    usuario = PerfilUsuarioSerializer(read_only=True)
    recurso = RecursoSerializer(read_only=True)

    # ====== ESCRITURA (lo que envía Angular) ======
    # usuario_id y recurso_id llegan desde el front
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=PerfilUsuario.objects.all(),
        source='usuario',          # se asigna al campo usuario del modelo
        write_only=True
    )
    recurso_id = serializers.PrimaryKeyRelatedField(
        queryset=Recurso.objects.all(),
        source='recurso',
        write_only=True
    )

    # El front usa "fecha_devolucion_estimada" pero el modelo usa "fecha_devolucion_esperada"
    fecha_devolucion_estimada = serializers.DateField(
        source='fecha_devolucion_esperada'
    )

    class Meta:
        model = Prestamo
        fields = [
            'id',

            # usuario / recurso
            'usuario', 'usuario_id',
            'recurso', 'recurso_id',

            # fechas
            'fecha_prestamo',           # solo lectura (auto_now_add)
            'fecha_devolucion_estimada',
            'fecha_devolucion_real',

            # control
            'estado',
            'renovaciones',
            'max_renovaciones',
            'notas',
            'bibliotecario_entrega',
            'bibliotecario_devolucion',
        ]
        extra_kwargs = {
            'fecha_prestamo': {'read_only': True},
        }
