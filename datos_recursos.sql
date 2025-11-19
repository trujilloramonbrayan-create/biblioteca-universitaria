SELECT *
FROM recursos_recurso;

SELECT
    r.id,
    r.titulo,
    r.autor,
    r.tipo,
    r.formato,
    r.codigo_interno,
    r.estado,
    r.numero_copias,
    r.copias_disponibles,
    COUNT(p.id) AS prestamos_activos
FROM recursos_recurso r
LEFT JOIN prestamos_prestamo p
       ON p.recurso_id = r.id
      AND p.estado = 'activo'
GROUP BY
    r.id, r.titulo, r.autor, r.tipo, r.formato,
    r.codigo_interno, r.estado, r.numero_copias, r.copias_disponibles
ORDER BY r.titulo;
