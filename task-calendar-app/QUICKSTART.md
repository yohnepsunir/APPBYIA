# 🚀 Quick Start Guide - Task Calendar App

## ⚡ Comandos Rápidos

### 🧪 Testing

```bash
# Todos los tests
cd backend && ./run_tests.sh

# Solo unitarios
./run_tests.sh --unit

# Solo integración
./run_tests.sh --integration

# Ver coverage HTML
./run_tests.sh && firefox htmlcov/index.html
```

### 🐳 Despliegue

```bash
# Desarrollo (hot reload)
./deploy.sh development

# Producción (optimizado)
./deploy.sh production

# Tests en Docker
./deploy.sh testing

# Todo junto
./deploy.sh full --build --logs
```

### 📊 Verificación

```bash
# Health check
curl http://localhost:5000/api/health

# Ver logs
docker-compose logs -f

# Stats
docker stats
```

## 📁 Archivos Clave

| Archivo | Descripción |
|---------|-------------|
| `backend/tests/` | Suite completa de tests |
| `pytest.ini` | Configuración pytest |
| `.coveragerc` | Configuración coverage |
| `run_tests.sh` | Script automatizado tests |
| `deploy.sh` | Script automatizado despliegue |
| `docker-compose.full.yml` | Compose completo |
| `Dockerfile.prod` | Docker optimizado |
| `.github/workflows/tests.yml` | CI/CD pipeline |

## 📚 Documentación

- **TESTING.md** - Guía completa de testing
- **DEPLOYMENT.md** - Guía de despliegue
- **README.md** - Documentación principal

## 🎯 Métricas del Proyecto

- ✅ **40+ tests** (unitarios + integración)
- ✅ **~85% coverage** de código
- ✅ **3 entornos** (dev, prod, test)
- ✅ **CI/CD** automatizado
- ✅ **Multi-platform** (Linux, Mac, Windows)

## 🔧 Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidas
├── unit/                    # Tests unitarios (24+)
│   ├── test_database.py     # 6 tests
│   ├── test_models.py       # 12 tests
│   └── test_routes.py       # 12 tests
└── integration/             # Tests integración (16+)
    ├── test_app_integration.py      # 8 tests
    └── test_task_workflow.py        # 8 tests
```

## 🎨 Comandos Docker

```bash
# Build
docker-compose build

# Up
docker-compose up -d

# Logs
docker-compose logs -f backend

# Shell
docker exec -it task-calendar-dev bash

# Clean
docker-compose down -v
```

## ✅ Checklist Pre-Despliegue

- [ ] Tests pasan: `./backend/run_tests.sh`
- [ ] Coverage > 80%
- [ ] Health check OK
- [ ] Docker build exitoso
- [ ] Logs sin errores

## 🐛 Troubleshooting Rápido

### Tests fallan
```bash
cd backend
pytest -vv  # Más detalle
pytest --lf  # Solo los que fallaron
```

### Puerto ocupado
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "5002:5000"
```

### Permisos
```bash
chmod +x deploy.sh backend/run_tests.sh
```

## 🚀 Workflow Típico

```bash
# 1. Desarrollo
./deploy.sh development

# 2. Hacer cambios en código

# 3. Ejecutar tests
cd backend && ./run_tests.sh

# 4. Si pasan, commit
git add .
git commit -m "Nueva funcionalidad"

# 5. Push (CI/CD automático)
git push

# 6. Desplegar producción
./deploy.sh production --build
```

---

**Tip**: Mantén este archivo abierto mientras desarrollas
