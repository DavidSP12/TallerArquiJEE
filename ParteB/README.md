# Parte B - Jakarta EE con Maven, WildFly y PostgreSQL

Este módulo implementa una aplicación Jakarta EE empaquetada como WAR, con persistencia en PostgreSQL y despliegue en WildFly.

La Parte B está organizada como proyecto Maven multi-módulo:

- demo: módulo servidor Jakarta EE que genera demo.war
- cliente-pesado: módulo cliente que depende de las clases compartidas del módulo demo

## Estructura

- [pom.xml](pom.xml): proyecto padre Maven
- [demo/pom.xml](demo/pom.xml): módulo WAR desplegable
- [cliente-pesado/pom.xml](cliente-pesado/pom.xml): módulo cliente
- [docker-compose.yml](docker-compose.yml): PostgreSQL + WildFly
- [demo/src/main/java/com/arquitaller/rest/ProductoResource.java](demo/src/main/java/com/arquitaller/rest/ProductoResource.java): endpoint REST principal

## Requisitos para entorno local o IDE

- JDK 25
- Maven 3.9 o superior
- Docker y Docker Compose
- IDE recomendado: IntelliJ IDEA, Eclipse o VS Code con soporte Java

## Flujo recomendado fuera de GitHub

1. Compilar la Parte B

~~~bash
cd ParteB
cd demo
chmod +x mvnw
./mvnw -B -ntp -f ../pom.xml clean package
~~~

Resultado esperado:

- Se genera el WAR en demo/target/demo.war
- Se generan clases compartidas para cliente-pesado durante la compilación multi-módulo

2. Levantar base de datos y WildFly

~~~bash
cd ParteB
docker compose up -d
~~~

3. Verificar que WildFly despliegue la aplicación

~~~bash
cd ParteB
docker compose logs -f wildfly-app
~~~

Cuando aparezca un mensaje de despliegue de demo.war, la aplicación está lista.

4. Probar endpoint REST

~~~bash
curl -i http://localhost:8080/demo/api/productos
~~~

5. Probar creación de producto

~~~bash
curl -i -X POST http://localhost:8080/demo/api/productos \
	-H "Content-Type: application/json" \
	-d '{"nombre":"Teclado","precio":120.5}'
~~~

6. Detener el entorno

~~~bash
cd ParteB
docker compose down -v
~~~

## Pruebas funcionales sugeridas

Antes de probar, confirma que el entorno está arriba:

~~~bash
cd ParteB && docker compose ps
~~~

### 1. Listar productos (GET)

Comando:

~~~bash
curl -i http://localhost:8080/demo/api/productos
~~~

Resultado esperado:

- Código HTTP 200
- Cuerpo JSON con una lista, por ejemplo: [] o [{"id":1,"nombre":"Teclado","precio":120.5}]

### 2. Crear producto válido (POST)

Comando:

~~~bash
curl -i -X POST http://localhost:8080/demo/api/productos \
	-H "Content-Type: application/json" \
	-d '{"nombre":"Mouse","precio":75.0}'
~~~

Resultado esperado:

- Código HTTP 201
- Cuerpo JSON con el producto creado

### 3. Validar persistencia después de crear (GET)

Comando:

~~~bash
curl -s http://localhost:8080/demo/api/productos
~~~

Resultado esperado:

- Debe aparecer el producto creado en la lista

### 4. Caso de error controlado (POST con JSON inválido)

Comando:

~~~bash
curl -i -X POST http://localhost:8080/demo/api/productos \
	-H "Content-Type: application/json" \
	-d '{"nombre":123,"precio":"abc"}'
~~~

Resultado esperado:

- Código HTTP 400 o 500, dependiendo de cómo procese el servidor el error de deserialización
- Si aparece 500 de forma constante, revisar logs de WildFly para agregar validaciones explícitas en el recurso

## Ejecución desde IDE

### Opción A: usar Maven del proyecto

1. Abrir [pom.xml](pom.xml) como proyecto Maven.
2. Configurar JDK del proyecto en versión 25.
3. Ejecutar ciclo Maven clean y package del proyecto padre.
4. Confirmar que existe demo/target/demo.war.

### Opción B: usar terminal integrada del IDE

Ejecutar exactamente estos comandos dentro del IDE:

~~~bash
cd ParteB/demo
chmod +x mvnw
./mvnw -B -ntp -f ../pom.xml clean package
cd ../
docker compose up -d
~~~

## Solución de problemas

- Error con mvnw y MavenWrapperMain:
	Ejecuta mvnw desde el directorio demo, porque ahí está su carpeta .mvn.

- Error de conexión a base de datos:
	Verifica que el contenedor db-servidor esté activo y puerto 5432 disponible.

- Endpoint no responde en 8080:
	Revisa logs de wildfly-app y confirma despliegue de demo.war.

## Comandos rápidos

Compilar:

~~~bash
cd ParteB/demo && chmod +x mvnw && ./mvnw -B -ntp -f ../pom.xml clean package
~~~

Levantar entorno:

~~~bash
cd ParteB && docker compose up -d
~~~

Probar API:

~~~bash
curl -i http://localhost:8080/demo/api/productos
~~~

Apagar entorno:

~~~bash
cd ParteB && docker compose down -v
~~~