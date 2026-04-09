package com.arquitaller.servicio;

import com.arquitaller.modelo.Producto;
import jakarta.ejb.Remote;
import java.util.List;

@Remote // Esta anotación indica que puede ser llamado desde fuera del servidor
public interface ProductoServiceRemote {
    List<Producto> obtenerTodos();
    void crearProducto(Producto producto);
}