# psi_1321_p02_p4
Repositorio para realizar la práctica P2 de la asignatura Proyecto de Sistemas Informáticos.

## Comandos

- Ejecución de pruebas
``
make clear_db
make clear_update_db
make test_datamodel
``

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
