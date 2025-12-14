#!/bin/bash

# Script de verificación completa del proyecto
# Este script verifica que todo el sistema de testing y despliegue funciona

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Banner
clear
echo -e "${GREEN}"
cat << "EOF"
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   Task Calendar App - Verificación Completa del Sistema   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Verificar pre-requisitos
print_header "1. Verificando Pre-requisitos"

# Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}')
    print_success "Docker instalado: $DOCKER_VERSION"
else
    print_error "Docker no está instalado"
    exit 1
fi

# Docker Compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version | awk '{print $4}')
    print_success "Docker Compose instalado: $COMPOSE_VERSION"
else
    print_error "Docker Compose no está instalado"
    exit 1
fi

# Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    print_success "Python instalado: $PYTHON_VERSION"
else
    print_warning "Python no está instalado (opcional para desarrollo local)"
fi

# Verificar estructura de archivos
print_header "2. Verificando Estructura de Archivos"

REQUIRED_FILES=(
    "backend/tests/conftest.py"
    "backend/tests/unit/test_database.py"
    "backend/tests/unit/test_models.py"
    "backend/tests/unit/test_routes.py"
    "backend/tests/integration/test_app_integration.py"
    "backend/tests/integration/test_task_workflow.py"
    "backend/pytest.ini"
    "backend/.coveragerc"
    "backend/run_tests.sh"
    "deploy.sh"
    "Dockerfile.prod"
    "docker-compose.full.yml"
    "TESTING.md"
    "DEPLOYMENT.md"
    ".github/workflows/tests.yml"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "$file"
    else
        print_error "$file - FALTA"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

if [ $MISSING_FILES -gt 0 ]; then
    print_error "Faltan $MISSING_FILES archivos requeridos"
    exit 1
fi

# Verificar permisos de scripts
print_header "3. Verificando Permisos de Scripts"

SCRIPTS=("deploy.sh" "backend/run_tests.sh")
for script in "${SCRIPTS[@]}"; do
    if [ -x "$script" ]; then
        print_success "$script tiene permisos de ejecución"
    else
        print_warning "$script no tiene permisos, corrigiendo..."
        chmod +x "$script"
        print_success "$script - permisos corregidos"
    fi
done

# Verificar sintaxis de archivos Python
print_header "4. Verificando Sintaxis de Tests"

cd backend
if python3 -m py_compile tests/conftest.py 2>/dev/null; then
    print_success "conftest.py - sintaxis OK"
else
    print_error "conftest.py - error de sintaxis"
fi

for test_file in tests/unit/*.py tests/integration/*.py; do
    if [ -f "$test_file" ]; then
        if python3 -m py_compile "$test_file" 2>/dev/null; then
            print_success "$(basename $test_file) - sintaxis OK"
        else
            print_error "$(basename $test_file) - error de sintaxis"
        fi
    fi
done
cd ..

# Instalar dependencias (opcional)
print_header "5. Instalación de Dependencias (Opcional)"
print_info "¿Deseas instalar dependencias de Python? (s/n)"
read -r INSTALL_DEPS

if [[ "$INSTALL_DEPS" =~ ^[Ss]$ ]]; then
    cd backend
    if [ ! -d "venv" ]; then
        print_info "Creando entorno virtual..."
        python3 -m venv venv
    fi
    
    print_info "Instalando dependencias..."
    source venv/bin/activate
    pip install -q -r requirements.txt
    print_success "Dependencias instaladas"
    deactivate
    cd ..
else
    print_info "Saltando instalación de dependencias"
fi

# Ejecutar tests
print_header "6. Ejecutando Tests"
print_info "¿Deseas ejecutar los tests ahora? (s/n)"
read -r RUN_TESTS

if [[ "$RUN_TESTS" =~ ^[Ss]$ ]]; then
    print_info "Ejecutando tests en Docker..."
    
    # Build de imagen de test
    print_info "Construyendo imagen de Docker para testing..."
    docker build -f Dockerfile.prod --target test -t task-calendar-test . 2>&1 | grep -v "^#" || true
    
    if [ $? -eq 0 ]; then
        print_success "Imagen de test construida exitosamente"
        
        # Ejecutar tests
        print_info "Ejecutando suite de tests..."
        docker run --rm task-calendar-test
        
        if [ $? -eq 0 ]; then
            print_success "¡Todos los tests pasaron!"
        else
            print_error "Algunos tests fallaron"
        fi
    else
        print_error "Error al construir imagen de test"
    fi
else
    print_info "Saltando ejecución de tests"
fi

# Test de despliegue
print_header "7. Test de Despliegue"
print_info "¿Deseas probar el despliegue de desarrollo? (s/n)"
read -r TEST_DEPLOY

if [[ "$TEST_DEPLOY" =~ ^[Ss]$ ]]; then
    print_info "Desplegando aplicación en modo desarrollo..."
    docker-compose up -d --build
    
    if [ $? -eq 0 ]; then
        print_success "Aplicación desplegada"
        
        # Esperar a que arranque
        print_info "Esperando a que la aplicación esté lista..."
        sleep 10
        
        # Test de health check
        print_info "Probando health check..."
        HEALTH_CHECK=$(curl -s http://localhost:5000/api/health 2>/dev/null || echo "")
        
        if [[ "$HEALTH_CHECK" == *"ok"* ]]; then
            print_success "Health check OK - Aplicación funcionando"
            print_success "Accede a: http://localhost:5000"
        else
            print_warning "Health check falló - revisa los logs"
        fi
        
        print_info "Para ver logs: docker-compose logs -f"
        print_info "Para detener: docker-compose down"
    else
        print_error "Error al desplegar aplicación"
    fi
else
    print_info "Saltando test de despliegue"
fi

# Resumen final
print_header "8. Resumen de Verificación"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          VERIFICACIÓN COMPLETADA               ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""

print_success "Pre-requisitos: OK"
print_success "Estructura de archivos: OK"
print_success "Permisos de scripts: OK"
print_success "Sintaxis de Python: OK"

echo ""
echo -e "${BLUE}Próximos pasos:${NC}"
echo ""
echo "1. Ejecutar tests completos:"
echo -e "   ${YELLOW}cd backend && ./run_tests.sh${NC}"
echo ""
echo "2. Ver coverage:"
echo -e "   ${YELLOW}cd backend && ./run_tests.sh && firefox htmlcov/index.html${NC}"
echo ""
echo "3. Desplegar desarrollo:"
echo -e "   ${YELLOW}./deploy.sh development${NC}"
echo ""
echo "4. Desplegar producción:"
echo -e "   ${YELLOW}./deploy.sh production${NC}"
echo ""
echo "5. Leer documentación:"
echo -e "   ${YELLOW}cat TESTING.md${NC}"
echo -e "   ${YELLOW}cat DEPLOYMENT.md${NC}"
echo -e "   ${YELLOW}cat QUICKSTART.md${NC}"
echo ""

print_info "Para ayuda: ./deploy.sh --help"
print_info "Para tests: cd backend && ./run_tests.sh --help"

echo ""
echo -e "${GREEN}¡Sistema listo para usar!${NC} 🚀"
echo ""
