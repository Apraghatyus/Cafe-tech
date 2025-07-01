CREATE TABLE public.productos (
  id          SERIAL PRIMARY KEY,
  nombre      VARCHAR(100) NOT NULL,
  precio      NUMERIC(10,2) NOT NULL,
  descripcion TEXT
);

CREATE TABLE public.pedidos (
  id             SERIAL PRIMARY KEY,
  cliente        VARCHAR(100) NOT NULL,
  producto_id    INT NOT NULL 
                   REFERENCES public.productos(id)
                     ON DELETE RESTRICT,
  cantidad       INT NOT NULL CHECK (cantidad > 0),
  fecha_entrega  DATE NOT NULL,
  estado         VARCHAR(50) NOT NULL
);

CREATE TABLE public.usuarios (
  id       SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(128) NOT null,
  role VARCHAR(10) not null
);