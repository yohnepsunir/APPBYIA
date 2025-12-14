# Task Calendar App - Complete Deployment Guide

## 🚀 Guía Completa de Despliegue

Esta guía cubre el despliegue completo de la aplicación Task Calendar App en diferentes entornos.

## 📋 Tabla de Contenidos

- [Pre-requisitos](#pre-requisitos)
- [Arquitectura](#arquitectura)
- [Entornos de Despliegue](#entornos-de-despliegue)
- [Despliegue Rápido](#despliegue-rápido)
- [Despliegue Detallado](#despliegue-detallado)
- [Configuración](#configuración)
- [Monitoreo](#monitoreo)
- [Troubleshooting](#troubleshooting)

## 🔧 Pre-requisitos

### Software Requerido

- **Docker**: >= 20.10
- **Docker Compose**: >= 2.0
- **Git**: >= 2.30
- **Python**: >= 3.9 (para desarrollo local)

### Verificar Instalación

```bash
docker --version
docker-compose --version
git --version
python --version
```

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│            Nginx (Opcional)             │
│          Reverse Proxy / SSL            │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼──────┐    ┌────────▼────────┐
│  Development │    │   Production    │
│   Container  │    │    Container    │
│  Port: 5000  │    │   Port: 5001    │
└───────┬──────┘    └────────┬────────┘
        │                     │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  SQLite Database    │
        │   (Volume Mounted)  │
        └─────────────────────┘
```

## 🎯 Entornos de Despliegue

### 1. Development (Desarrollo)

- Hot reload activado
- Debug mode ON
- Logs verbosos
- Sin optimizaciones

**Puerto**: 5000

### 2. Production (Producción)

- Optimizado para rendimiento
- Debug mode OFF
- Health checks
- Usuario no-root

**Puerto**: 5001

### 3. Testing (Pruebas)

- Ejecuta suite de tests
- No expone puertos
- Se destruye después de ejecutar

## ⚡ Despliegue Rápido

### Opción 1: Script de Despliegue Automático

```bash
# Dar permisos de ejecución
chmod +x deploy.sh

# Desarrollo
./deploy.sh development

# Producción
./deploy.sh production

# Tests
./deploy.sh testing

# Entorno completo (dev + prod + nginx)
./deploy.sh full
```

### Opción 2: Docker Compose Manual

```bash
# Desarrollo
docker-compose up -d

# Desarrollo con archivo completo
docker-compose -f docker-compose.full.yml up -d backend-dev

# Producción
docker-compose -f docker-compose.full.yml up -d backend-prod

# Tests
docker-compose -f docker-compose.full.yml --profile testing run --rm backend-test
```

## 📖 Despliegue Detallado

### 1. Clonar Repositorio

```bash
git clone https://github.com/yohnepsunir/APPBYIA.git
cd APPBYIA/task-calendar-app
```

### 2. Configurar Variables de Entorno (Opcional)

Crear archivo `.env`:

```bash
# Development
FLASK_ENV=development
FLASK_DEBUG=1

# Production
# FLASK_ENV=production
# FLASK_DEBUG=0

# Database
DATABASE_PATH=/app/data/tasks.db

# Security (cambiar en producción)
SECRET_KEY=your-secret-key-here
```

### 3. Despliegue de Desarrollo

```bash
# Método 1: Script
./deploy.sh development --build --logs

# Método 2: Docker Compose
docker-compose -f docker-compose.full.yml up -d backend-dev --build

# Verificar
curl http://localhost:5000/api/health
```

**Características**:
- ✅ Auto-reload al cambiar código
- ✅ Volúmenes montados para desarrollo
- ✅ Logs en tiempo real
- ✅ Base de datos persistente

### 4. Despliegue de Producción

```bash
# Paso 1: Ejecutar tests
./deploy.sh testing

# Paso 2: Desplegar
./deploy.sh production --build

# Verificar health
curl http://localhost:5001/api/health
```

**Características**:
- ✅ Imagen optimizada multi-stage
- ✅ Usuario no-root (seguridad)
- ✅ Health checks automáticos
- ✅ Restart automático
- ✅ Sin debug mode

### 5. Despliegue con Nginx (Producción Completa)

```bash
# Desplegar stack completo
./deploy.sh full --build

# O manualmente
docker-compose -f docker-compose.full.yml --profile production up -d
```

**Acceder**:
- Frontend/API: http://localhost
- Backend directo: http://localhost:5001

**Configuración SSL** (para HTTPS):

1. Generar certificados:
```bash
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem
```

2. Descomentar sección HTTPS en `nginx/nginx.conf`

3. Reiniciar Nginx:
```bash
docker-compose -f docker-compose.full.yml restart nginx
```

## ⚙️ Configuración

### Configuración de Base de Datos

La base de datos SQLite se almacena en volúmenes de Docker:

```yaml
volumes:
  db_data_dev:    # Desarrollo
  db_data_prod:   # Producción
```

**Backup de Base de Datos**:

```bash
# Desarrollo
docker cp task-calendar-dev:/app/tasks.db ./backup-dev.db

# Producción
docker cp task-calendar-prod:/app/tasks.db ./backup-prod.db
```

**Restaurar Base de Datos**:

```bash
# Desarrollo
docker cp ./backup-dev.db task-calendar-dev:/app/tasks.db

# Producción
docker cp ./backup-prod.db task-calendar-prod:/app/tasks.db
docker-compose -f docker-compose.full.yml restart backend-prod
```

### Configuración de Logs

**Ver logs en tiempo real**:

```bash
# Desarrollo
docker-compose -f docker-compose.full.yml logs -f backend-dev

# Producción
docker-compose -f docker-compose.full.yml logs -f backend-prod

# Nginx
docker-compose -f docker-compose.full.yml logs -f nginx
```

**Logs persistentes**:

Agregar a `docker-compose.full.yml`:

```yaml
services:
  backend-prod:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Escalabilidad

**Escalar instancias**:

```bash
# Escalar a 3 instancias
docker-compose -f docker-compose.full.yml up -d --scale backend-prod=3

# Nginx balanceará automáticamente
```

## 📊 Monitoreo

### Health Checks

**Verificar estado**:

```bash
# Development
curl http://localhost:5000/api/health

# Production
curl http://localhost:5001/api/health

# Respuesta esperada:
# {"status":"ok"}
```

**Health check automático Docker**:

```bash
# Ver estado de salud
docker ps

# Inspeccionar health
docker inspect task-calendar-prod | grep -A 10 Health
```

### Monitoreo de Recursos

```bash
# Ver uso de recursos
docker stats

# Ver procesos
docker-compose -f docker-compose.full.yml ps

# Inspeccionar container
docker inspect task-calendar-prod
```

### Logs y Debugging

```bash
# Logs de errores
docker-compose -f docker-compose.full.yml logs backend-prod | grep ERROR

# Últimas 100 líneas
docker-compose -f docker-compose.full.yml logs --tail=100 backend-prod

# Ejecutar comando dentro del container
docker exec -it task-calendar-prod bash

# Ver variables de entorno
docker exec task-calendar-prod env
```

## 🐛 Troubleshooting

### Problema: Puerto ya en uso

```bash
# Encontrar proceso usando el puerto
sudo lsof -i :5000

# Matar proceso
sudo kill -9 PID

# O cambiar puerto en docker-compose.yml
ports:
  - "5002:5000"  # Usar puerto 5002 en lugar de 5000
```

### Problema: Container no inicia

```bash
# Ver logs detallados
docker logs task-calendar-prod

# Verificar configuración
docker-compose -f docker-compose.full.yml config

# Reiniciar desde cero
docker-compose -f docker-compose.full.yml down -v
docker-compose -f docker-compose.full.yml up -d --build
```

### Problema: Base de datos corrupta

```bash
# Detener container
docker-compose -f docker-compose.full.yml stop backend-prod

# Eliminar volumen (PERDERÁS DATOS)
docker volume rm task-calendar-app_db_data_prod

# Reiniciar
docker-compose -f docker-compose.full.yml up -d backend-prod
```

### Problema: Tests fallan

```bash
# Ejecutar tests con más detalle
docker-compose -f docker-compose.full.yml --profile testing run --rm backend-test -vv

# Ejecutar un test específico
docker-compose -f docker-compose.full.yml --profile testing run --rm backend-test \
  python -m pytest tests/unit/test_models.py -v
```

### Problema: Permisos en Linux

```bash
# Cambiar ownership
sudo chown -R $USER:$USER .

# Dar permisos a scripts
chmod +x deploy.sh
chmod +x backend/run_tests.sh
```

## 🔄 Actualizaciones

### Actualizar la aplicación

```bash
# Pull última versión
git pull origin main

# Rebuild y restart
./deploy.sh production --build --clean

# O manualmente
docker-compose -f docker-compose.full.yml down
docker-compose -f docker-compose.full.yml up -d --build backend-prod
```

### Rollback

```bash
# Ver versiones de imágenes
docker images | grep task-calendar

# Usar imagen anterior
docker tag task-calendar-app:old task-calendar-app:latest
docker-compose -f docker-compose.full.yml up -d backend-prod
```

## 🔒 Seguridad

### Mejores Prácticas

1. **No usar root**:
   - ✅ Implementado en Dockerfile.prod con usuario `appuser`

2. **Variables de entorno**:
```bash
# Usar archivo .env (no commitear)
echo ".env" >> .gitignore
```

3. **Actualizar dependencias**:
```bash
cd backend
pip list --outdated
pip install -U package-name
pip freeze > requirements.txt
```

4. **Escanear vulnerabilidades**:
```bash
# Scan de imagen Docker
docker scan task-calendar-app:latest

# Scan de dependencias Python
pip install safety
safety check -r backend/requirements.txt
```

5. **HTTPS en producción**:
   - Usar certificados SSL
   - Configurar Nginx con SSL
   - Forzar HTTPS redirect

## 📈 Optimizaciones

### Performance

```dockerfile
# En Dockerfile.prod
# - Multi-stage build: ✅
# - Slim base image: ✅
# - No cache pip: ✅
# - Layer caching: ✅
```

### Base de Datos

```python
# Optimizar queries
# Agregar índices en database.py
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

### Nginx Caching

Ya configurado en `nginx/nginx.conf`:
- Compresión gzip
- Cache de estáticos
- No cache de API

## 📚 Comandos Útiles

```bash
# Ver todos los containers
docker ps -a

# Limpiar sistema Docker
docker system prune -a --volumes

# Ver volúmenes
docker volume ls

# Ver networks
docker network ls

# Stats en tiempo real
docker stats

# Exportar/Importar imagen
docker save task-calendar-app:latest > backup.tar
docker load < backup.tar

# Ejecutar shell en container
docker exec -it task-calendar-prod /bin/bash
```

## 🤝 Soporte

Para problemas o preguntas:

1. Revisar esta documentación
2. Ver logs: `docker-compose logs -f`
3. Abrir issue en GitHub
4. Revisar TESTING.md para pruebas

---

**Última actualización**: Diciembre 2025
**Versión**: 1.0
