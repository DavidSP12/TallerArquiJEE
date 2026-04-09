# Parte A - Cliente y servidor gRPC con Docker

Este proyecto implementa una solución cliente-servidor con RPC usando gRPC.

## Qué incluye

- **Servidor gRPC**: consulta su base de datos SQLite y devuelve la lista de estudiantes.
- **Cliente gRPC**: pide los estudiantes al servidor y los guarda en su propia base SQLite.
- **Prueba de carga**: ejecuta muchas peticiones en paralelo para medir el servidor.

## Estructura

- `proto/students.proto`: contrato del servicio gRPC.
- `server/`: servidor y base de datos SQLite de origen.
- `client/`: cliente y base de datos SQLite destino.
- `load_test/`: herramienta de prueba de carga.
- `docker-compose.yml`: despliegue de los servicios.

## Levantar servidor y cliente

Desde `ParteA/`:

```bash
docker compose up --build server client
```

Salida esperada:

- El servidor inicia en el puerto `50051`.
- El cliente se conecta al servidor, obtiene estudiantes y los guarda en su base de datos.

## Ejecutar prueba de carga

```bash
docker compose --profile load run --rm load-tester
```

Variables de entorno para ajustar la carga:

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

## Verificar datos de la base del cliente

```bash
docker compose run --rm client python -c "import sqlite3; c=sqlite3.connect('/data/client.db'); print(c.execute('select * from students').fetchall())"
```

## Detener y limpiar

```bash
docker compose down -v
```
