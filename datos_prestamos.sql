SELECT * FROM prestamos_prestamo;

SELECT 
    p.id,
    u.id AS perfil_id,
    authu.username,
    authu.first_name AS nombre,
    authu.last_name AS apellido,
    r.titulo AS recurso,
    p.fecha_prestamo,
    p.fecha_devolucion_esperada,
    p.estado
FROM prestamos_prestamo p
JOIN usuarios_perfilusuario u ON p.usuario_id = u.id
JOIN auth_user authu ON u.usuario_id = authu.id
JOIN recursos_recurso r ON p.recurso_id = r.id;
