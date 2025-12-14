#!/bin/bash

# Script para ejecutar todos los tests
# Uso: ./run_tests.sh [options]

set -e  # Salir si hay algún error

echo "======================================"
echo "Task Calendar App - Test Suite"
echo "======================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Cambiar al directorio backend
cd "$(dirname "$0")"

# Verificar que estamos en el directorio correcto
if [ ! -f "requirements.txt" ]; then
    print_error "No se encontró requirements.txt. Ejecuta este script desde el directorio backend."
    exit 1
fi

# Opción de ayuda
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    echo "Uso: ./run_tests.sh [opciones]"
    echo ""
    echo "Opciones:"
    echo "  -u, --unit           Ejecutar solo tests unitarios"
    echo "  -i, --integration    Ejecutar solo tests de integración"
    echo "  -c, --coverage       Generar reporte de cobertura completo"
    echo "  -f, --fast           Ejecutar tests rápidos (sin coverage)"
    echo "  -v, --verbose        Modo verbose"
    echo "  -h, --help           Mostrar esta ayuda"
    echo ""
    exit 0
fi

# Verificar que pytest está instalado
if ! python -m pytest --version > /dev/null 2>&1; then
    print_warning "pytest no está instalado. Instalando dependencias..."
    pip install -r requirements.txt
fi

# Variables
RUN_UNIT=true
RUN_INTEGRATION=true
WITH_COVERAGE=true
VERBOSE=""

# Procesar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--unit)
            RUN_UNIT=true
            RUN_INTEGRATION=false
            shift
            ;;
        -i|--integration)
            RUN_UNIT=false
            RUN_INTEGRATION=true
            shift
            ;;
        -c|--coverage)
            WITH_COVERAGE=true
            shift
            ;;
        -f|--fast)
            WITH_COVERAGE=false
            shift
            ;;
        -v|--verbose)
            VERBOSE="-vv"
            shift
            ;;
        *)
            print_error "Opción desconocida: $1"
            exit 1
            ;;
    esac
done

# Limpiar archivos de coverage anteriores
print_status "Limpiando archivos de cobertura anteriores..."
rm -f .coverage
rm -rf htmlcov
rm -f coverage.xml

# Ejecutar tests unitarios
if [ "$RUN_UNIT" = true ]; then
    print_status "Ejecutando tests unitarios..."
    if [ "$WITH_COVERAGE" = true ]; then
        python -m pytest tests/unit/ $VERBOSE --cov=. --cov-report=term-missing --cov-report=html --cov-config=.coveragerc
    else
        python -m pytest tests/unit/ $VERBOSE
    fi
    UNIT_EXIT=$?
    
    if [ $UNIT_EXIT -eq 0 ]; then
        print_status "✓ Tests unitarios pasaron exitosamente"
    else
        print_error "✗ Tests unitarios fallaron"
        exit $UNIT_EXIT
    fi
    echo ""
fi

# Ejecutar tests de integración
if [ "$RUN_INTEGRATION" = true ]; then
    print_status "Ejecutando tests de integración..."
    if [ "$WITH_COVERAGE" = true ]; then
        python -m pytest tests/integration/ $VERBOSE --cov=. --cov-append --cov-report=term-missing --cov-report=html --cov-config=.coveragerc
    else
        python -m pytest tests/integration/ $VERBOSE
    fi
    INTEGRATION_EXIT=$?
    
    if [ $INTEGRATION_EXIT -eq 0 ]; then
        print_status "✓ Tests de integración pasaron exitosamente"
    else
        print_error "✗ Tests de integración fallaron"
        exit $INTEGRATION_EXIT
    fi
    echo ""
fi

# Reporte de cobertura
if [ "$WITH_COVERAGE" = true ]; then
    print_status "Generando reporte de cobertura..."
    python -m coverage report
    echo ""
    print_status "Reporte HTML generado en: htmlcov/index.html"
    
    # Generar XML para CI/CD
    python -m coverage xml
    print_status "Reporte XML generado: coverage.xml"
fi

echo ""
print_status "======================================"
print_status "Todos los tests completados exitosamente!"
print_status "======================================"
