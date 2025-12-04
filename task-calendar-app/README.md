# Task Calendar App

## Descripción General

**Task Calendar App** es una aplicación web para la gestión de tareas y calendario, desarrollada íntegramente con la asistencia de inteligencia artificial (IA). Todo el código, la estructura y la documentación fueron generados mediante instrucciones y prompts dirigidos a una IA, sin intervención manual en la edición del código por parte del usuario. Este proyecto demuestra cómo la IA puede ser utilizada como herramienta principal para diseñar, implementar y corregir aplicaciones web modernas.

## Características
- Interfaz de tres columnas:
  - Lista de tareas
  - Formulario de edición de tareas
  - Panel de archivos adjuntos
- Cada tarea incluye:
  - Título
  - Descripción
  - Categoría
  - Prioridad (1-5)
  - Fecha de vencimiento
  - Estado
- Funcionalidad completa de gestión de tareas (CRUD)
- Soporte de almacenamiento local para persistencia de tareas
- Dockerización para despliegue local sencillo

## Estructura del Proyecto
```
task-calendar-app
├── backend
│   ├── app.py
│   ├── models.py
│   ├── database.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── tasks.py
│   ├── requirements.txt
│   └── .env
├── frontend
│   ├── index.html
│   ├── css
│   │   └── styles.css
│   ├── js
│   │   ├── app.js
│   │   ├── api.js
│   │   └── storage.js
│   └── assets
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```

## Cómo Ejecutar la Aplicación

### Requisitos Previos
- Docker
- Docker Compose

### Instalación y Ejecución
1. Clona el repositorio:
   ```
   git clone https://github.com/yohnepsunir/APPBYIA.git
   cd task-calendar-app
   ```

2. Construye y ejecuta la aplicación con Docker Compose:
   ```
   docker-compose up --build
   ```

3. Accede a la aplicación en tu navegador en `http://localhost:5000`.

### Uso
- Utiliza la interfaz para agregar nuevas tareas, editar las existentes y gestionar tu lista de tareas.
- Las tareas se almacenan en el almacenamiento local del navegador para mantener la persistencia entre sesiones.

## Contribuciones
¡Las contribuciones son bienvenidas! Puedes enviar un pull request o abrir un issue para sugerencias, mejoras o corrección de errores.

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

---

> **Nota:** Todo el desarrollo, corrección y documentación de esta aplicación se realizó exclusivamente mediante interacción con IA, sin edición manual de código.