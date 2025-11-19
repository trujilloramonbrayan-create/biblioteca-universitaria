import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_backend.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario
from recursos.models import Recurso
from prestamos.models import Prestamo, Reserva, Sancion

def crear_datos():
    print("🔧 Creando datos de prueba...")
    
    # Limpiar datos anteriores
    User.objects.filter(username__in=['maria.garcia', 'juan.perez', 'carlos.lopez']).delete()
    
    # === USUARIOS ===
    print("👤 Usuarios...")
    
    # Estudiante 1
    maria = User.objects.create_user('maria.garcia', 'maria@uni.edu', 'pass123')
    maria.first_name, maria.last_name = 'María', 'García'
    maria.save()
    PerfilUsuario.objects.create(
        usuario=maria, 
        rol='estudiante',
        codigo_universitario='20220001',
        programa_academico='Ingeniería de Sistemas'
    )
    
    # Estudiante 2
    juan = User.objects.create_user('juan.perez', 'juan@uni.edu', 'pass123')
    juan.first_name, juan.last_name = 'Juan', 'Pérez'
    juan.save()
    PerfilUsuario.objects.create(
        usuario=juan,
        rol='estudiante',
        codigo_universitario='20220002',
        programa_academico='Administración'
    )
    
    # Bibliotecario
    carlos = User.objects.create_user('carlos.lopez', 'carlos@uni.edu', 'pass123')
    carlos.first_name, carlos.last_name = 'Carlos', 'López'
    carlos.is_staff = True
    carlos.save()
    PerfilUsuario.objects.create(
        usuario=carlos,
        rol='bibliotecario',
        codigo_universitario='BIB001'
    )
    
    # === RECURSOS ===
    print("📚 Recursos...")
    
    libro1 = Recurso.objects.create(
        titulo='Cien Años de Soledad',
        autor='Gabriel García Márquez',
        tipo='libro',
        formato='fisico',
        isbn='9780307474728',
        codigo_interno='LIB-001',
        editorial='Sudamericana',
        anio_publicacion=1967,
        categoria='Literatura',
        ubicacion='Estante A1',
        numero_copias=3,
        copias_disponibles=3,
        palabras_clave='literatura, colombia'
    )
    
    libro2 = Recurso.objects.create(
        titulo='Python para Todos',
        autor='John Zelle',
        tipo='libro',
        formato='fisico',
        isbn='9781590282410',
        codigo_interno='LIB-002',
        editorial='Franklin',
        anio_publicacion=2016,
        categoria='Informática',
        ubicacion='Estante B3',
        numero_copias=5,
        copias_disponibles=4,
        palabras_clave='python, programación'
    )
    
    ebook = Recurso.objects.create(
        titulo='Clean Code',
        autor='Robert Martin',
        tipo='ebook',
        formato='digital',
        codigo_interno='EBOOK-001',
        anio_publicacion=2008,
        categoria='Informática',
        url_acceso='https://ejemplo.com/clean-code.pdf',
        numero_copias=999,
        copias_disponibles=999,
        palabras_clave='programación, buenas prácticas'
    )
    
    # === PRÉSTAMOS ===
    print("📖 Préstamos...")
    
    # Activo
    p1 = Prestamo.objects.create(
        usuario=maria,
        recurso=libro2,
        fecha_devolucion_esperada=timezone.now().date() + timedelta(days=7),
        estado='activo',
        bibliotecario_entrega=carlos
    )
    libro2.copias_disponibles -= 1
    libro2.veces_prestado += 1
    libro2.save()
    
    # Vencido
    p2 = Prestamo.objects.create(
        usuario=juan,
        recurso=libro1,
        fecha_devolucion_esperada=timezone.now().date() - timedelta(days=3),
        estado='vencido',
        bibliotecario_entrega=carlos
    )
    libro1.copias_disponibles -= 1
    libro1.veces_prestado += 1
    libro1.save()
    
    # === RESERVA ===
    print("📅 Reservas...")
    
    Reserva.objects.create(
        usuario=maria,
        recurso=libro1,
        fecha_expiracion=timezone.now() + timedelta(days=2),
        estado='pendiente'
    )
    
    # === SANCIÓN ===
    print("⚠️ Sanciones...")
    
    Sancion.objects.create(
        usuario=juan,
        prestamo=p2,
        tipo='retraso',
        descripcion='Retraso de 3 días',
        fecha_fin=timezone.now().date() + timedelta(days=7),
        dias_sancion=7,
        multa=15000.00
    )
    
    juan.perfil.sancionado = True
    juan.perfil.fecha_fin_sancion = timezone.now().date() + timedelta(days=7)
    juan.perfil.save()
    
    # === RESUMEN ===
    print("\n✅ DATOS CREADOS:")
    print(f"   • {User.objects.count()} usuarios")
    print(f"   • {Recurso.objects.count()} recursos")
    print(f"   • {Prestamo.objects.count()} préstamos")
    print(f"   • {Reserva.objects.count()} reservas")
    print(f"   • {Sancion.objects.count()} sanciones")
    
    print("\n🔑 CREDENCIALES:")
    print("   admin / admin123")
    print("   maria.garcia / pass123")
    print("   juan.perez / pass123 (SANCIONADO)")
    print("   carlos.lopez / pass123 (Bibliotecario)")
    print("\n🚀 Ejecuta: python manage.py runserver")

if __name__ == '__main__':
    try:
        crear_datos()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()