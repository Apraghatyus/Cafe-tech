-- 0) auth for join session
INSERT INTO public.usuarios (username, password, role)
VALUES (
  'Apraghatyus',
  '1143877959',
  'admin'
);

-- 1) Productos de ejemplo
INSERT INTO public.productos (nombre, precio, descripcion) VALUES
  ('Café Arábica', 12.50, 'Tostado medio, sabor suave'),
  ('Té Verde',    8.20,  'Hojas premium de Japón'),
  ('Chocolate',  15.00,  '70% cacao, sin azúcar');

-- 2) Pedidos de ejemplo (asegúrate de que producto_id exista)
INSERT INTO public.pedidos (cliente, producto_id, cantidad, fecha_entrega, estado) VALUES
  ('María López', 1,  3, '2025-07-10', 'pendiente'),
  ('Juan Pérez',  2,  1, '2025-07-05', 'enviado'),
  ('Ana Torres',  3, 10, '2025-07-15', 'entregado');