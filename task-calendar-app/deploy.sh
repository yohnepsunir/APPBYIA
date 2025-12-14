#!/bin/bash

# Script de despliegue para diferentes entornos
# Uso: ./deploy.sh [development|production|testing]

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Función de ayuda
show_help() {
    echo "Task Calendar App - Script de Despliegue"
    echo ""
    echo "Uso: ./deploy.sh [ENVIRONMENT] [OPTIONS]"
    echo ""
    echo "Environments:"
    echo "  development    Despliegue de desarrollo (hot reload, debug)"
    echo "  production     Despliegue de producción (optimizado, sin debug)"
    echo "  testing        Ejecutar tests en contenedor"
    echo ""
    echo "Options:"
    echo "  --build        Forzar rebuild de imágenes"
    echo "  --clean        Limpiar contenedores y volúmenes anteriores"
    echo "  --logs         Mostrar logs después del despliegue"
    echo "  --help         Mostrar esta ayuda"
    echo ""
    exit 0
}

# Variables por defecto
ENVIRONMENT=${1:-development}
BUILD_FLAG=""
CLEAN_FLAG=false
SHOW_LOGS=false

# Procesar argumentos
shift || true
while [[ $# -gt 0 ]]; do
    case $1 in
        --build)
            BUILD_FLAG="--build"
            shift
            ;;
        --clean)
            CLEAN_FLAG=true
            shift
            ;;
        --logs)
            SHOW_LOGS=true
            shift
            ;;
        --help)
            show_help
            ;;
        *)
            print_error "Opción desconocida: $1"
            exit 1
            ;;
    esac
done

print_info "======================================"
print_info "Task Calendar App - Despliegue"
print_info "Entorno: $ENVIRONMENT"
print_info "======================================"
echo ""

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado"
    exit 1
fi

# Limpiar si se solicita
if [ "$CLEAN_FLAG" = true ]; then
    print_warning "Limpiando contenedores y volúmenes anteriores..."
    docker-compose -f docker-compose.full.yml down -v 2>/dev/null || true
    docker-compose down -v 2>/dev/null || true
    print_success "Limpieza completada"
    echo ""
fi

# Despliegue según el entorno
case $ENVIRONMENT in
    development|dev)
        print_info "Desplegando entorno de DESARROLLO..."
        docker-compose -f docker-compose.full.yml up -d backend-dev $BUILD_FLAG
        
        if [ $? -eq 0 ]; then
            print_success "Aplicación desplegada en modo desarrollo"
            print_info "Accede a: http://localhost:5000"
            print_info "API Health: http://localhost:5000/api/health"
            print_info ""
            print_info "Para ver logs: docker-compose -f docker-compose.full.yml logs -f backend-dev"
        else
            print_error "Error en el despliegue"
            exit 1
        fi
        ;;
    
    production|prod)
        print_info "Desplegando entorno de PRODUCCIÓN..."
        
        # Ejecutar tests primero
        print_info "Ejecutando tests antes del despliegue..."
        docker-compose -f docker-compose.full.yml --profile testing run --rm backend-test
        
        if [ $? -ne 0 ]; then
            print_error "Los tests fallaron. Abortando despliegue."
            exit 1
        fi
        
        print_success "Tests pasaron exitosamente"
        
        # Desplegar producción
        docker-compose -f docker-compose.full.yml up -d backend-prod $BUILD_FLAG
        
        if [ $? -eq 0 ]; then
            print_success "Aplicación desplegada en modo producción"
            print_info "Accede a: http://localhost:5001"
            print_info "API Health: http://localhost:5001/api/health"
            print_info ""
            print_info "Para ver logs: docker-compose -f docker-compose.full.yml logs -f backend-prod"
            
            # Verificar health check
            print_info "Verificando health check..."
            sleep 5
            if curl -f http://localhost:5001/api/health &> /dev/null; then
                print_success "Health check OK"
            else
                print_warning "Health check falló. Revisa los logs."
            fi
        else
            print_error "Error en el despliegue"
            exit 1
        fi
        ;;
    
    testing|test)
        print_info "Ejecutando TESTS en contenedor..."
        docker-compose -f docker-compose.full.yml --profile testing run --rm backend-test $BUILD_FLAG
        
        if [ $? -eq 0 ]; then
            print_success "Todos los tests pasaron"
        else
            print_error "Algunos tests fallaron"
            exit 1
        fi
        ;;
    
    full)
        print_info "Desplegando entorno COMPLETO (dev + prod + nginx)..."
        
        # Tests
        print_info "Ejecutando tests..."
        docker-compose -f docker-compose.full.yml --profile testing run --rm backend-test
        
        if [ $? -ne 0 ]; then
            print_error "Tests fallaron. Abortando."
            exit 1
        fi
        
        # Desplegar todo
        docker-compose -f docker-compose.full.yml --profile production up -d $BUILD_FLAG
        
        if [ $? -eq 0 ]; then
            print_success "Entorno completo desplegado"
            print_info "Desarrollo: http://localhost:5000"
            print_info "Producción: http://localhost:5001"
            print_info "Nginx: http://localhost:80"
        else
            print_error "Error en el despliegue"
            exit 1
        fi
        ;;
    
    *)
        print_error "Entorno desconocido: $ENVIRONMENT"
        print_info "Usa: development, production, testing, o full"
        exit 1
        ;;
esac

# Mostrar logs si se solicita
if [ "$SHOW_LOGS" = true ]; then
    echo ""
    print_info "Mostrando logs... (Ctrl+C para salir)"
    sleep 2
    
    case $ENVIRONMENT in
        development|dev)
            docker-compose -f docker-compose.full.yml logs -f backend-dev
            ;;
        production|prod)
            docker-compose -f docker-compose.full.yml logs -f backend-prod
            ;;
        full)
            docker-compose -f docker-compose.full.yml --profile production logs -f
            ;;
    esac
fi

echo ""
print_success "======================================"
print_success "Despliegue completado exitosamente!"
print_success "======================================"
