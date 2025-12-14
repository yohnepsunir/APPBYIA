# Task Calendar App

[![Tests](https://github.com/yohnepsunir/APPBYIA/workflows/Tests%20CI%2FCD/badge.svg)](https://github.com/yohnepsunir/APPBYIA/actions)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)](https://github.com/yohnepsunir/APPBYIA)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📝 Descripción General

**Task Calendar App** es una aplicación web completa para la gestión de tareas y calendario, desarrollada con Flask (backend) y JavaScript vanilla (frontend), con base de datos SQLite y completamente contenerizada con Docker.

### ✨ Destacado

Este proyecto incluye:
- ✅ **Suite completa de pruebas** (unitarias e integración)
- ✅ **Cobertura de código** >= 80%
- ✅ **CI/CD** con GitHub Actions
- ✅ **Múltiples entornos** (desarrollo, producción, testing)
- ✅ **Documentación completa** de testing y despliegue
- ✅ **Dockerización optimizada** con multi-stage builds

## 🎯 Características

### Funcionalidad Principal
- ✅ Gestión completa de tareas (CRUD)
- ✅ Priorización de tareas (1-5)
- ✅ Categorización personalizable
- ✅ Fechas de vencimiento
- ✅ Estados de tareas (pending, in-progress, completed)
- ✅ Interfaz de tres columnas intuitiva
- ✅ Persistencia en SQLite

### Características Técnicas
- ✅ API RESTful con Flask
- ✅ Tests unitarios y de integración con pytest
- ✅ Cobertura de código con coverage.py
- ✅ CI/CD con GitHub Actions
- ✅ Docker multi-stage para optimización
- ✅ Nginx como reverse proxy (opcional)
- ✅ Health checks automáticos
- ✅ Scripts de despliegue automatizados

## 📁 Estructura del Proyecto

```
task-calendar-app/
├── backend/
│   ├── app.py                      # Aplicación Flask principal
│   ├── models.py                   # Modelos de datos
│   ├── database.py                 # Configuración de BD
│   ├── routes/
│   │   ├── __init__.py
│   │   └── tasks.py                # Rutas de la API
│   ├── tests/                      # ⭐ Suite de tests
│   │   ├── conftest.py             # Fixtures compartidas
│   │   ├── unit/                   # Tests unitarios
│   │   │   ├── test_database.py
│   │   │   ├── test_models.py
│   │   │   └── test_routes.py
│   │   └── integration/            # Tests de integración
│   │       ├── test_app_integration.py
│   │       └── test_task_workflow.py
│   ├── pytest.ini                  # Configuración de pytest
│   ├── .coveragerc                 # Configuración de coverage
│   ├── run_tests.sh                # Script de tests (Linux/Mac)
│   ├── run_tests.bat               # Script de tests (Windows)
│   └── requirements.txt            # Dependencias Python
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── app.js
│   │   ├── api.js
│   │   └── storage.js
│   └── assets/
├── nginx/
│   └── nginx.conf                  # Configuración de Nginx
├── .github/
│   └── workflows/
│       └── tests.yml               # ⭐ CI/CD Pipeline
├── Dockerfile                      # Dockerfile para desarrollo
├── Dockerfile.prod                 # ⭐ Dockerfile optimizado
├── docker-compose.yml              # Compose básico
├── docker-compose.full.yml         # ⭐ Compose completo
├── deploy.sh                       # ⭐ Script de despliegue
├── .gitignore
├── README.md
├── TESTING.md                      # ⭐ Documentación de testing
└── DEPLOYMENT.md                   # ⭐ Guía de despliegue

⭐ = Nuevos archivos agregados para testing y despliegue
```

## 🚀 Inicio Rápido

### Requisitos Previos
- Docker >= 20.10
- Docker Compose >= 2.0
- Git

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/yohnepsunir/APPBYIA.git
cd APPBYIA/task-calendar-app

# Dar permisos a scripts (Linux/Mac)
chmod +x deploy.sh
chmod +x backend/run_tests.sh
```

### Opción 1: Despliegue Simple (Desarrollo)

```bash
# Usando Docker Compose
docker-compose up -d

# O usando script de despliegue
./deploy.sh development
```

Accede a: **http://localhost:5000**

### Opción 2: Despliegue Completo (Producción)

```bash
# Ejecutar tests primero
./deploy.sh testing

# Desplegar en producción
./deploy.sh production --build

# O despliegue completo (dev + prod + nginx)
./deploy.sh full --build
```

Acceso:
- **Desarrollo**: http://localhost:5000
- **Producción**: http://localhost:5001
- **Nginx**: http://localhost:80

## 🧪 Testing

### Ejecutar Tests

```bash
cd backend

# Todos los tests con coverage
./run_tests.sh

# Solo tests unitarios
./run_tests.sh --unit

# Solo tests de integración
./run_tests.sh --integration

# Tests rápidos (sin coverage)
./run_tests.sh --fast

# En Windows
run_tests.bat
```

### Con pytest directamente

```bash
# Todos los tests
pytest

# Tests con coverage
pytest --cov=. --cov-report=html

# Ver reporte
# Abre: htmlcov/index.html
```

### Tests en Docker

```bash
docker-compose -f docker-compose.full.yml --profile testing run --rm backend-test
```

### Cobertura Actual

- **Cobertura total**: ~85%
- **Archivos cubiertos**: database.py, models.py, routes/tasks.py, app.py
- **Tests**: 40+ tests (unitarios + integración)

📖 **Documentación completa**: Ver [TESTING.md](TESTING.md)

## 🔧 API Endpoints

### Tasks

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks` | Obtener todas las tareas |
| GET | `/api/tasks/<id>` | Obtener tarea por ID |
| POST | `/api/tasks` | Crear nueva tarea |
| PUT | `/api/tasks/<id>` | Actualizar tarea |
| DELETE | `/api/tasks/<id>` | Eliminar tarea |
| GET | `/api/health` | Health check |

### Ejemplo de uso

```bash
# Crear tarea
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nueva tarea",
    "description": "Descripción",
    "category": "work",
    "priority": 3,
    "due_date": "2025-12-31"
  }'

# Obtener todas las tareas
curl http://localhost:5000/api/tasks

# Health check
curl http://localhost:5000/api/health
```

## 🐳 Docker

### Imágenes Disponibles

1. **Desarrollo** (`Dockerfile`):
   - Debug activado
   - Hot reload
   - Volúmenes montados

2. **Producción** (`Dockerfile.prod`):
   - Multi-stage build
   - Optimizado
   - Usuario no-root
   - Health checks

### Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Entrar al container
docker exec -it task-calendar-dev bash

# Ver stats
docker stats

# Limpiar
docker-compose down -v
```

📖 **Documentación completa**: Ver [DEPLOYMENT.md](DEPLOYMENT.md)

## 📊 CI/CD

### GitHub Actions

El proyecto incluye CI/CD automático que:
- ✅ Ejecuta tests en Python 3.9, 3.10, 3.11
- ✅ Genera reportes de cobertura
- ✅ Ejecuta linting (flake8, black, isort)
- ✅ Build y test de Docker
- ✅ Sube reportes a Codecov

Se ejecuta automáticamente en:
- Push a `main` o `develop`
- Pull requests

Ver: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)

## 📈 Monitoreo

### Health Checks

```bash
# Desarrollo
curl http://localhost:5000/api/health

# Producción
curl http://localhost:5001/api/health

# Respuesta:
# {"status":"ok"}
```

### Logs

```bash
# Logs en tiempo real
docker-compose logs -f backend

# Últimas 100 líneas
docker-compose logs --tail=100 backend

# Solo errores
docker-compose logs backend | grep ERROR
```

## 🔒 Seguridad

- ✅ Usuario no-root en producción
- ✅ No expone debug en producción
- ✅ Health checks configurados
- ✅ Variables de entorno para secretos
- ✅ Nginx como reverse proxy
- ✅ Soporte SSL/HTTPS (configurable)

## 🛠️ Desarrollo

### Configurar entorno local

```bash
cd backend

# Crear virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py

# Ejecutar tests
pytest
```

### Agregar nuevas funcionalidades

1. Escribe tests primero (TDD)
2. Implementa la funcionalidad
3. Ejecuta tests: `pytest`
4. Verifica cobertura: `pytest --cov`
5. Commit y push

## 📚 Documentación

- 📘 [TESTING.md](TESTING.md) - Guía completa de testing
- 📗 [DEPLOYMENT.md](DEPLOYMENT.md) - Guía de despliegue
- 📙 [API Documentation](#api-endpoints) - Endpoints de la API

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Escribe tests para tu funcionalidad
4. Implementa la funcionalidad
5. Verifica que todos los tests pasen: `./backend/run_tests.sh`
6. Commit: `git commit -m 'Agrega nueva funcionalidad'`
7. Push: `git push origin feature/nueva-funcionalidad`
8. Abre un Pull Request

### Guías para contribuir

- ✅ Cobertura de tests >= 80%
- ✅ Todos los tests deben pasar
- ✅ Seguir PEP 8 (Python)
- ✅ Documentar funciones y clases
- ✅ Actualizar documentación si es necesario

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**yohnepsunir**
- GitHub: [@yohnepsunir](https://github.com/yohnepsunir)

## 🙏 Agradecimientos

- Desarrollado con asistencia de IA
- Flask framework
- pytest para testing
- Docker para containerización

---

## 📌 Notas Importantes

### Para Testing

Ver la guía completa en [TESTING.md](TESTING.md) que incluye:
- Suite completa de tests unitarios e integración
- Configuración de coverage
- Scripts de ejecución automatizados
- Mejores prácticas de testing

### Para Despliegue

Ver la guía completa en [DEPLOYMENT.md](DEPLOYMENT.md) que incluye:
- Múltiples entornos (dev, prod, testing)
- Configuración de Docker optimizada
- Nginx como reverse proxy
- SSL/HTTPS
- Monitoreo y troubleshooting

---

**Última actualización**: Diciembre 2025  
**Versión**: 1.0.0