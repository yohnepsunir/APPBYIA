# Task Calendar App - Guía de Testing

## 📋 Tabla de Contenidos

- [Introducción](#introducción)
- [Estructura de Tests](#estructura-de-tests)
- [Instalación](#instalación)
- [Ejecutar Tests](#ejecutar-tests)
- [Tipos de Tests](#tipos-de-tests)
- [Coverage](#coverage)
- [CI/CD](#cicd)
- [Mejores Prácticas](#mejores-prácticas)

## 🎯 Introducción

Este proyecto cuenta con un conjunto completo de pruebas unitarias e integración que garantizan la calidad y funcionamiento correcto de la aplicación de calendario de tareas.

### Tecnologías Utilizadas

- **pytest**: Framework de testing principal
- **pytest-cov**: Plugin para cobertura de código
- **pytest-flask**: Utilidades para testing de Flask
- **pytest-mock**: Mocking simplificado
- **coverage**: Análisis de cobertura de código

## 📁 Estructura de Tests

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Fixtures compartidas
│   ├── unit/                    # Tests unitarios
│   │   ├── __init__.py
│   │   ├── test_database.py     # Tests de base de datos
│   │   ├── test_models.py       # Tests de modelos
│   │   └── test_routes.py       # Tests de rutas/endpoints
│   └── integration/             # Tests de integración
│       ├── __init__.py
│       ├── test_app_integration.py     # Tests de la app completa
│       └── test_task_workflow.py       # Tests de flujos de trabajo
├── pytest.ini                   # Configuración de pytest
├── .coveragerc                  # Configuración de coverage
├── run_tests.sh                 # Script para Linux/Mac
└── run_tests.bat                # Script para Windows
```

## 🚀 Instalación

### Instalar Dependencias

```bash
cd backend
pip install -r requirements.txt
```

Las dependencias de testing incluyen:
- pytest==7.4.3
- pytest-cov==4.1.0
- pytest-flask==1.3.0
- pytest-mock==3.12.0
- coverage==7.3.2

## ▶️ Ejecutar Tests

### Opción 1: Scripts de Conveniencia

#### Linux/Mac:
```bash
cd backend
chmod +x run_tests.sh
./run_tests.sh                 # Todos los tests con coverage
./run_tests.sh --unit          # Solo tests unitarios
./run_tests.sh --integration   # Solo tests de integración
./run_tests.sh --fast          # Tests sin coverage (más rápido)
./run_tests.sh --verbose       # Modo verbose
```

#### Windows:
```cmd
cd backend
run_tests.bat                  # Todos los tests con coverage
run_tests.bat --unit           # Solo tests unitarios
run_tests.bat --integration    # Solo tests de integración
run_tests.bat --fast           # Tests sin coverage
```

### Opción 2: Comandos Directos con pytest

```bash
cd backend

# Ejecutar todos los tests
pytest

# Tests unitarios con coverage
pytest tests/unit/ -v --cov=. --cov-report=term-missing

# Tests de integración
pytest tests/integration/ -v

# Test específico
pytest tests/unit/test_models.py::TestTaskModel::test_task_creation -v

# Tests con markers
pytest -m unit              # Solo tests marcados como 'unit'
pytest -m integration       # Solo tests marcados como 'integration'
pytest -m "not slow"        # Excluir tests lentos
```

### Opción 3: Con Docker

```bash
# Construir imagen
docker-compose build

# Ejecutar tests en container
docker-compose run backend python -m pytest tests/ -v

# Ejecutar con coverage
docker-compose run backend python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

## 🧪 Tipos de Tests

### Tests Unitarios

Prueban componentes individuales de forma aislada:

- **test_database.py**: Pruebas de conexión y estructura de base de datos
- **test_models.py**: Pruebas de modelos (CRUD de tareas)
- **test_routes.py**: Pruebas de endpoints de la API

**Ejemplo de ejecución:**
```bash
pytest tests/unit/ -v
```

### Tests de Integración

Prueban el flujo completo de la aplicación:

- **test_app_integration.py**: Integración de toda la aplicación
- **test_task_workflow.py**: Flujos de trabajo completos (crear → actualizar → eliminar)

**Ejemplo de ejecución:**
```bash
pytest tests/integration/ -v
```

## 📊 Coverage (Cobertura de Código)

### Generar Reporte de Cobertura

```bash
cd backend

# Generar coverage en terminal
pytest --cov=. --cov-report=term-missing

# Generar reporte HTML
pytest --cov=. --cov-report=html

# Generar reporte XML (para CI/CD)
pytest --cov=. --cov-report=xml

# Ver reporte HTML en navegador
# El archivo se genera en: htmlcov/index.html
```

### Interpretar Reportes de Coverage

- **Stmts**: Número total de líneas de código
- **Miss**: Líneas no cubiertas por tests
- **Cover**: Porcentaje de cobertura
- **Missing**: Números de línea específicos no cubiertos

**Objetivo de cobertura**: >= 80%

### Archivos de Configuración

**`.coveragerc`**: Configura qué archivos incluir/excluir
- Excluye directorios de tests, venv, __pycache__
- Configura formato de reportes
- Define líneas a ignorar (pragma: no cover)

## 🔄 CI/CD

### GitHub Actions

El proyecto incluye un workflow de CI/CD en `.github/workflows/tests.yml`:

**Características:**
- ✅ Ejecuta tests en múltiples versiones de Python (3.9, 3.10, 3.11)
- ✅ Tests unitarios e integración
- ✅ Análisis de cobertura
- ✅ Linting (flake8, black, isort)
- ✅ Build y test de Docker
- ✅ Upload de reportes a Codecov

**Se ejecuta en:**
- Push a `main` o `develop`
- Pull requests a `main` o `develop`

### Badges de Estado

Agrega estos badges a tu README.md:

```markdown
![Tests](https://github.com/yohnepsunir/APPBYIA/workflows/Tests%20CI%2FCD/badge.svg)
[![codecov](https://codecov.io/gh/yohnepsunir/APPBYIA/branch/main/graph/badge.svg)](https://codecov.io/gh/yohnepsunir/APPBYIA)
```

## 📝 Mejores Prácticas

### 1. Escribir Tests Efectivos

```python
# ✅ BIEN: Test específico y descriptivo
def test_task_creation_with_valid_data(self, db_connection, sample_task_data):
    """Test que verifica la creación exitosa de una tarea con datos válidos"""
    task_id = Task.create(**sample_task_data)
    assert task_id > 0
    
    task = Task.get_by_id(task_id)
    assert task['title'] == sample_task_data['title']

# ❌ MAL: Test vago y sin verificaciones suficientes
def test_task(self):
    task_id = Task.create('Test', '', '', 1, '')
    assert task_id
```

### 2. Usar Fixtures Apropiadamente

```python
# Definir en conftest.py
@pytest.fixture(scope='function')
def sample_task_data():
    return {
        'title': 'Test Task',
        'description': 'Test description',
        'category': 'work',
        'priority': 3,
        'due_date': '2025-12-31'
    }

# Usar en tests
def test_create_task(self, sample_task_data):
    task_id = Task.create(**sample_task_data)
    assert task_id > 0
```

### 3. Organización de Tests

- **Un archivo de test por módulo** que estás probando
- **Una clase de test por clase** del código
- **Nombres descriptivos** que explican qué se está probando
- **Arrange-Act-Assert** pattern

```python
def test_task_update(self):
    # Arrange: Preparar datos
    task_id = Task.create('Original', 'Desc', 'cat', 3, '2025-12-31')
    
    # Act: Ejecutar acción
    Task.update(task_id, 'Updated', 'Desc', 'cat', 3, '2025-12-31', 'completed')
    
    # Assert: Verificar resultado
    task = Task.get_by_id(task_id)
    assert task['title'] == 'Updated'
    assert task['status'] == 'completed'
```

### 4. Tests Independientes

Cada test debe poder ejecutarse de forma independiente:

```python
# ✅ BIEN: Crea sus propios datos
def test_get_task(self, db_connection):
    task_id = Task.create('Test', '', '', 3, '')
    task = Task.get_by_id(task_id)
    assert task is not None

# ❌ MAL: Depende de datos de otros tests
def test_get_task_bad(self):
    task = Task.get_by_id(1)  # Asume que existe
    assert task is not None
```

### 5. Manejo de Base de Datos en Tests

```python
# Usar fixture que crea DB limpia para cada test
@pytest.fixture(scope='function')
def db_connection():
    db_fd, db_path = tempfile.mkstemp()
    database.DATABASE = db_path
    init_db()
    
    yield db_path
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
```

## 🐛 Debugging de Tests

### Ver output detallado
```bash
pytest -v -s  # -s muestra prints
```

### Ejecutar tests hasta el primer fallo
```bash
pytest -x
```

### Ejecutar solo tests que fallaron la última vez
```bash
pytest --lf
```

### Debugger interactivo
```bash
pytest --pdb  # Abre debugger en fallos
```

### Ver traceback completo
```bash
pytest --tb=long
```

## 📈 Métricas y Reportes

### Estadísticas de Tests
```bash
pytest --durations=10  # Muestra los 10 tests más lentos
```

### Generar Reporte JUnit (para CI)
```bash
pytest --junitxml=junit.xml
```

### Análisis de Cobertura Detallado
```bash
coverage report --show-missing
coverage html
```

## 🔧 Troubleshooting

### Problema: Tests fallan con "ModuleNotFoundError"
**Solución**: Asegúrate de ejecutar pytest desde el directorio `backend/`

### Problema: Base de datos bloqueada
**Solución**: Verifica que los fixtures cierren las conexiones correctamente

### Problema: Tests pasan individualmente pero fallan en conjunto
**Solución**: Revisa que los tests sean independientes y no compartan estado

### Problema: Coverage bajo
**Solución**: 
- Ejecuta `coverage report --show-missing` para ver líneas no cubiertas
- Agrega tests para casos edge y error handling

## 📚 Recursos Adicionales

- [Documentación de pytest](https://docs.pytest.org/)
- [pytest-flask](https://pytest-flask.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Testing Flask Applications](https://flask.palletsprojects.com/en/2.3.x/testing/)

## 🤝 Contribuir

Al agregar nuevas funcionalidades:

1. ✅ Escribe tests ANTES de implementar (TDD)
2. ✅ Asegura coverage >= 80%
3. ✅ Ejecuta todos los tests antes de commit
4. ✅ Actualiza esta documentación si es necesario

---

**Última actualización**: Diciembre 2025
