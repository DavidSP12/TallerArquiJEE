package com.arquitaller.cliente;

import com.arquitaller.modelo.Producto;
import com.arquitaller.servicio.ProductoServiceRemote;

import javax.naming.Context;
import javax.naming.InitialContext;
import java.util.List;
import java.util.Properties;

public class ClienteMain {

    public static void main(String[] args) {
        try {
            // 1. Configurar las propiedades para conectarse a Wildfly
            Properties jndiProps = new Properties();
            jndiProps.put(Context.INITIAL_CONTEXT_FACTORY, "org.wildfly.naming.client.WildFlyInitialContextFactory");
            jndiProps.put(Context.PROVIDER_URL, "http-remoting://localhost:8080");

            // Si Wildfly pide credenciales más adelante, se descomentan estas líneas:
            // jndiProps.put(Context.SECURITY_PRINCIPAL, "admin");
            // jndiProps.put(Context.SECURITY_CREDENTIALS, "admin123");

            // 2. Crear el contexto inicial
            System.out.println("Conectando al servidor Wildfly...");
            Context ctx = new InitialContext(jndiProps);

            // 3. Definir la cadena de búsqueda JNDI
            // Formato: ejb:/[nombre-del-war]/[NombreDeLaClaseEJB]![PaqueteCompletoDeLaInterfazRemota]
            String jndiName = "ejb:/demo/ProductoService!com.arquitaller.servicio.ProductoServiceRemote";

            System.out.println("Buscando el EJB: " + jndiName);
            ProductoServiceRemote servicio = (ProductoServiceRemote) ctx.lookup(jndiName);

            // 4. Probar la lógica de negocio a través de la red
            System.out.println("EJB encontrado. Creando producto de prueba...");

            Producto nuevoProducto = new Producto("Laptop Gamer Asux", 1500.50);
            servicio.crearProducto(nuevoProducto);
            System.out.println("Producto enviado al servidor exitosamente.");

            System.out.println("Consultando todos los productos almacenados...");
            List<Producto> productos = servicio.obtenerTodos();

            System.out.println("--- LISTA DE PRODUCTOS ---");
            for (Producto p : productos) {
                System.out.println("ID: " + p.getId() + " | Nombre: " + p.getNombre() + " | Precio: $" + p.getPrecio());
            }

        } catch (Exception e) {
            System.err.println("Error al conectar o ejecutar el EJB remoto:");
            e.printStackTrace();
        }
    }
}