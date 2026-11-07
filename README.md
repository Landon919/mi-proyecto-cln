# Sazón Urbano - Proyecto Integrador de Aprendizaje (Equipo 3)

Implementación de una solución de software basada en lógica de negocio (DDD, Specification, State Machine) con API REST.

## Requisitos Previos
* Docker y Docker Compose
* Python 3.10+ (si se ejecuta localmente sin Docker)

## Instrucciones de Instalación y Ejecución
Para levantar la base de datos, la API y ejecutar las pruebas en un entorno reproducible (12-Factor App):

1. Clona este repositorio.
2. Copia el archivo `.env.example` y renómbralo a `.env`.
3. Ejecuta el siguiente comando en la terminal:
   ```bash
   docker-compose up --build