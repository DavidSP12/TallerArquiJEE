package com.arquitaller.rest;

import com.arquitaller.modelo.Producto;
import com.arquitaller.servicio.ProductoServiceRemote;
import jakarta.ejb.EJB;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import java.util.List;

@Path("/productos") // La ruta final será: http://localhost:8080/demo/api/productos
@Produces(MediaType.APPLICATION_JSON) // Devuelve datos en formato JSON
@Consumes(MediaType.APPLICATION_JSON) // Recibe datos en formato JSON
public class ProductoResource {

    // Inyectamos el EJB que ya contiene la lógica de base de datos
    @EJB
    private ProductoServiceRemote productoService;

    @GET
    public Response obtenerTodos() {
        List<Producto> lista = productoService.obtenerTodos();
        return Response.ok(lista).build();
    }

    @POST
    public Response crearProducto(Producto producto) {
        try {
            productoService.crearProducto(producto);
            return Response.status(Response.Status.CREATED).entity(producto).build();
        } catch (Exception e) {
            return Response.serverError().entity("Error al crear el producto").build();
        }
    }
}