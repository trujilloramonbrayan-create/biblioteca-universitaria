-- Script para crear las tablas en biblioteca_db
-- Ejecutar este script DESPUÉS de crear la base de datos

-- IMPORTANTE: Ya debes estar conectado a biblioteca_db en pgAdmin

-- Tabla de usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('estudiante', 'docente', 'bibliotecario', 'administrador')),
    codigo_institucional VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT true,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de categorías
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de recursos bibliográficos
CREATE TABLE recursos (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    editorial VARCHAR(100),
    año_publicacion INTEGER,
    categoria_id INTEGER REFERENCES categorias(id) ON DELETE SET NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('fisico', 'digital')),
    ubicacion VARCHAR(100),
    ejemplares_totales INTEGER DEFAULT 1 CHECK (ejemplares_totales >= 0),
    ejemplares_disponibles INTEGER DEFAULT 1 CHECK (ejemplares_disponibles >= 0),
    portada_url VARCHAR(500),
    descripcion TEXT,
    idioma VARCHAR(50) DEFAULT 'Español',
    numero_paginas INTEGER,
    activo BOOLEAN DEFAULT true,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de préstamos
CREATE TABLE prestamos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE NOT NULL,
    recurso_id INTEGER REFERENCES recursos(id) ON DELETE CASCADE NOT NULL,
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion_prevista TIMESTAMP NOT NULL,
    fecha_devolucion_real TIMESTAMP,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo' CHECK (estado IN ('activo', 'devuelto', 'retrasado', 'cancelado')),
    renovaciones INTEGER DEFAULT 0 CHECK (renovaciones >= 0),
    dias_retraso INTEGER DEFAULT 0,
    multa_aplicada DECIMAL(10, 2) DEFAULT 0.00,
    notas TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de reservas
CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE NOT NULL,
    recurso_id INTEGER REFERENCES recursos(id) ON DELETE CASCADE NOT NULL,
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'activa' CHECK (estado IN ('activa', 'completada', 'cancelada', 'expirada')),
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de historial de acciones (auditoría)
CREATE TABLE historial_acciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    accion VARCHAR(100) NOT NULL,
    tabla_afectada VARCHAR(50),
    registro_id INTEGER,
    detalles JSONB,
    ip_address VARCHAR(45),
    fecha_accion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_codigo ON usuarios(codigo_institucional);
CREATE INDEX idx_usuarios_rol ON usuarios(rol);

CREATE INDEX idx_recursos_titulo ON recursos(titulo);
CREATE INDEX idx_recursos_autor ON recursos(autor);
CREATE INDEX idx_recursos_isbn ON recursos(isbn);
CREATE INDEX idx_recursos_categoria ON recursos(categoria_id);
CREATE INDEX idx_recursos_disponibilidad ON recursos(ejemplares_disponibles);

CREATE INDEX idx_prestamos_usuario ON prestamos(usuario_id);
CREATE INDEX idx_prestamos_recurso ON prestamos(recurso_id);
CREATE INDEX idx_prestamos_estado ON prestamos(estado);
CREATE INDEX idx_prestamos_fecha_devolucion ON prestamos(fecha_devolucion_prevista);

CREATE INDEX idx_reservas_usuario ON reservas(usuario_id);
CREATE INDEX idx_reservas_recurso ON reservas(recurso_id);
CREATE INDEX idx_reservas_estado ON reservas(estado);

-- Insertar datos iniciales

-- Categorías iniciales
INSERT INTO categorias (nombre, descripcion) VALUES
('Ciencias de la Computación', 'Libros relacionados con programación, algoritmos, bases de datos'),
('Matemáticas', 'Libros de álgebra, cálculo, estadística'),
('Ingeniería', 'Libros de ingeniería en general'),
('Literatura', 'Novelas, cuentos, poesía'),
('Historia', 'Libros de historia universal y local'),
('Ciencias Naturales', 'Biología, química, física'),
('Administración', 'Gestión empresarial, economía'),
('Derecho', 'Legislación, jurisprudencia');

-- Usuario administrador inicial (password: admin123)
-- Nota: En Django, este hash será generado automáticamente
INSERT INTO usuarios (username, email, password_hash, nombre, apellido, rol, codigo_institucional) VALUES
('admin', 'admin@biblioteca.edu.co', 'pbkdf2_sha256$600000$temp$hash', 'Administrador', 'Sistema', 'administrador', 'ADM001');

-- Comentarios sobre las contraseñas
COMMENT ON COLUMN usuarios.password_hash IS 'Hash de contraseña generado por Django';

-- Vista para recursos disponibles
CREATE VIEW vista_recursos_disponibles AS
SELECT 
    r.id,
    r.isbn,
    r.titulo,
    r.autor,
    r.editorial,
    r.año_publicacion,
    c.nombre as categoria,
    r.tipo,
    r.ejemplares_totales,
    r.ejemplares_disponibles,
    r.ubicacion
FROM recursos r
LEFT JOIN categorias c ON r.categoria_id = c.id
WHERE r.activo = true AND r.ejemplares_disponibles > 0;

-- Vista para préstamos activos
CREATE VIEW vista_prestamos_activos AS
SELECT 
    p.id,
    u.nombre || ' ' || u.apellido as usuario,
    u.codigo_institucional,
    r.titulo as libro,
    p.fecha_prestamo,
    p.fecha_devolucion_prevista,
    CASE 
        WHEN p.fecha_devolucion_prevista < CURRENT_TIMESTAMP THEN 'RETRASADO'
        ELSE 'ACTIVO'
    END as estado_real,
    CASE 
        WHEN p.fecha_devolucion_prevista < CURRENT_TIMESTAMP 
        THEN EXTRACT(DAY FROM CURRENT_TIMESTAMP - p.fecha_devolucion_prevista)
        ELSE 0
    END as dias_retraso
FROM prestamos p
JOIN usuarios u ON p.usuario_id = u.id
JOIN recursos r ON p.recurso_id = r.id
WHERE p.estado IN ('activo', 'retrasado');

-- Función para actualizar ejemplares disponibles
CREATE OR REPLACE FUNCTION actualizar_disponibilidad_recurso()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT' AND NEW.estado = 'activo') THEN
        UPDATE recursos 
        SET ejemplares_disponibles = ejemplares_disponibles - 1
        WHERE id = NEW.recurso_id AND ejemplares_disponibles > 0;
    ELSIF (TG_OP = 'UPDATE' AND OLD.estado = 'activo' AND NEW.estado = 'devuelto') THEN
        UPDATE recursos 
        SET ejemplares_disponibles = ejemplares_disponibles + 1
        WHERE id = NEW.recurso_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para mantener disponibilidad actualizada
CREATE TRIGGER trigger_actualizar_disponibilidad
AFTER INSERT OR UPDATE ON prestamos
FOR EACH ROW
EXECUTE FUNCTION actualizar_disponibilidad_recurso();

-- Función para verificar disponibilidad antes de préstamo
CREATE OR REPLACE FUNCTION verificar_disponibilidad()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT ejemplares_disponibles FROM recursos WHERE id = NEW.recurso_id) <= 0 THEN
        RAISE EXCEPTION 'No hay ejemplares disponibles para este recurso';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para verificar disponibilidad
CREATE TRIGGER trigger_verificar_disponibilidad
BEFORE INSERT ON prestamos
FOR EACH ROW
EXECUTE FUNCTION verificar_disponibilidad();

-- Permisos básicos
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE '✅ Base de datos biblioteca_db creada exitosamente';
    RAISE NOTICE '✅ Tablas creadas: usuarios, categorias, recursos, prestamos, reservas, historial_acciones';
    RAISE NOTICE '✅ Índices y triggers configurados';
    RAISE NOTICE '✅ Datos iniciales insertados';
END $$;


-- Para saber que datos existen en la tabla de categorias
-- SELECT * FROM categorias;