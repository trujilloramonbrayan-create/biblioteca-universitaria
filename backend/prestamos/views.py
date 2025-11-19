from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Prestamo
from .serializers import PrestamoSerializer


@api_view(['GET'])
def listar_prestamos(request):
    prestamos = Prestamo.objects.all()
    serializer = PrestamoSerializer(prestamos, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def crear_prestamo(request):
    serializer = PrestamoSerializer(data=request.data)
    if serializer.is_valid():
        prestamo = serializer.save()
        # devolvemos el préstamo ya con usuario y recurso anidados
        return Response(PrestamoSerializer(prestamo).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
def actualizar_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    # partial=True para permitir actualizar solo algunos campos (estado, fecha, etc.)
    serializer = PrestamoSerializer(prestamo, data=request.data, partial=True)
    if serializer.is_valid():
        prestamo = serializer.save()
        return Response(PrestamoSerializer(prestamo).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    prestamo.delete()
    return Response({"mensaje": "Eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
