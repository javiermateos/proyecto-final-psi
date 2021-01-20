# Proyecto de Sistemas Informáticos 

Repositorio para realizar el proyecto de la asignatura Proyecto de Sistemas Informáticos
de la [Escuela Politécnica Superior](https://www.uam.es/ss/Satellite/EscuelaPolitecnica/es/home.html)
de la [UAM](https://www.uam.es/UAM/Home.htm?language=es).

## Requisitos

- Python 3.6
- PostgreSQL >= 11.0

Si por el contrario quieres probar el proyecto con docker:
- Docker: 20.X.X
- Docker compose: 1.27

## Preparación

Lo mejor para usar el proyecto y verlo es utilizar docker, ya que de otra forma
necesitarías tener instalado localmente los requisitos expuestos más arriba, así
como crear un entorno virtual para ello.

### Comandos (Docker)
```sh
git clone https://github.com/javiermateos/psi-final-project.git
cd psi-final-project
make run
# En otra terminal ejecuta los siguientes comandos:
make update_db
make populate
make create_super_user
```
Tras ejecutar los comandos puedes entrar al proyecto en http://localhost:8000.
Puedes loguearte con cualquiera de los usuarios que están en el archivo
[19-edat_psi](./labassign/19-edat_psi.csv).

Para realizar los test:
```sh
make test_datamodel
make tests_services
```

**Importante**: para parar los servicios de docker debes emplear el comando:
```sh
make stop
```

## Requisitos Funcionales:

- Existen dos tipos de usuarios en la aplicación: usuarios registrados y usuarios
  no registrados. 
- Los usuarios registrados se identificarán usando un nombre de usuario (NIE) y 
  una clave (DNI).
- Los usuarios no registrados solo podrán acceder al login y al home.

A partir de aquí se entiende que los requisitos se refieren únicamente a los usuarios
registrados de la aplicación.

- Los usuarios podrán solicitar la convalidación de prácticas que se le concederá
  si cumplen con unos criterios preestablecidos.
- Los usuarios deben poder agruparse en parejas.
- Los usuarios deben poder cancelar la pareja a la que pertenecen.
- Los usuarios podrán solicitar grupos de prácticas asignandose de forma inmediata
  por orden de llegada.
- Cuando un estudiante se elimine de la aplicación todas las parejas a las que 
  pertenezcan deberán eliminarse.

## Notas adicionales

Los comandos y pasos realizados para hacer el proyecto se han recogido en el documento
[Notes](./notes.md).
