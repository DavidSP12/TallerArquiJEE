# Parte A - Cliente/Servidor gRPC con Docker

Este proyecto implementa una arquitectura cliente-servidor usando RPC con gRPC.

## Componentes

- **Servidor gRPC**: consulta su base de datos SQLite y retorna la lista de estudiantes.
- **Cliente gRPC**: solicita estudiantes al servidor y los inserta/actualiza en su base SQLite.
- **Load tester**: ejecuta pruebas de carga concurrentes sobre el endpoint gRPC del servidor.

## Estructura

- `proto/students.proto`: contrato del servicio gRPC.
- `server/`: servicio servidor + BD SQLite de origen.
- `client/`: aplicación cliente + BD SQLite destino.
- `load_test/`: herramienta de prueba de carga.
- `docker-compose.yml`: orquestación de servicios.

## Levantar servidor y cliente

Desde `ParteA/`:

```bash
docker compose up --build server client
```

Salida esperada:

- El servidor inicia en el puerto `50051`.
- El cliente se conecta al servidor, obtiene estudiantes y los guarda en su BD.

## Ejecutar prueba de carga

```bash
docker compose --profile load run --rm load-tester
```

Variables de entorno disponibles para ajustar carga:

- `LOAD_USERS` (por defecto: `100`)
- `LOAD_REQUESTS_PER_USER` (por defecto: `200`)
- `LOAD_TIMEOUT` (por defecto: `5` segundos)

Ejemplo personalizado:

```bash
docker compose --profile load run --rm \
  -e LOAD_USERS=200 \
  -e LOAD_REQUESTS_PER_USER=300 \
  load-tester
```

## Verificar datos de la BD del cliente

```bash
docker compose run --rm client python -c "import sqlite3; c=sqlite3.connect('/data/client.db'); print(c.execute('select * from students').fetchall())"
```

## Detener y limpiar

```bash
docker compose down -v
```
