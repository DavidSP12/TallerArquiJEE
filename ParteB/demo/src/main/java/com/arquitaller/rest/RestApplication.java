package com.arquitaller.rest;

import jakarta.annotation.sql.DataSourceDefinition;
import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;

@DataSourceDefinition(
        name = "java:jboss/datasources/ExampleDS", // Sobrescribimos el DataSource por defecto
        className = "org.postgresql.ds.PGSimpleDataSource", // Usaremos el driver de PostgreSQL
        url = "jdbc:postgresql://db-servidor:5432/appdb", // 'db-servidor' es el nombre del contenedor en docker-compose
        user = "admin",
        password = "password"
)
@ApplicationPath("/api")
public class RestApplication extends Application {
}