package com.arquitaller.servicio;

import com.arquitaller.modelo.Producto;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import java.util.List;

@Stateless // Define que es un EJB sin estado
public class ProductoService implements ProductoServiceRemote {

    // Inyecta el contexto de JPA configurado en el persistence.xml
    @PersistenceContext(unitName = "MiUnidadPersistencia")
    private EntityManager em;

    @Override
    public List<Producto> obtenerTodos() {
        return em.createQuery("SELECT p FROM Producto p", Producto.class).getResultList();
    }

    @Override
    public void crearProducto(Producto producto) {
        em.persist(producto);
    }
}