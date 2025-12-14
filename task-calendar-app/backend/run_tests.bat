@echo off
REM Script para ejecutar tests en Windows
REM Uso: run_tests.bat [options]

echo ======================================
echo Task Calendar App - Test Suite
echo ======================================
echo.

cd /d "%~dp0"

REM Verificar que estamos en el directorio correcto
if not exist "requirements.txt" (
    echo [ERROR] No se encontro requirements.txt
    exit /b 1
)

REM Verificar argumentos
set RUN_UNIT=1
set RUN_INTEGRATION=1
set WITH_COVERAGE=1

:parse_args
if "%1"=="-u" (
    set RUN_UNIT=1
    set RUN_INTEGRATION=0
    shift
    goto parse_args
)
if "%1"=="--unit" (
    set RUN_UNIT=1
    set RUN_INTEGRATION=0
    shift
    goto parse_args
)
if "%1"=="-i" (
    set RUN_UNIT=0
    set RUN_INTEGRATION=1
    shift
    goto parse_args
)
if "%1"=="--integration" (
    set RUN_UNIT=0
    set RUN_INTEGRATION=1
    shift
    goto parse_args
)
if "%1"=="-f" (
    set WITH_COVERAGE=0
    shift
    goto parse_args
)
if "%1"=="--fast" (
    set WITH_COVERAGE=0
    shift
    goto parse_args
)

REM Limpiar coverage
echo [INFO] Limpiando archivos de cobertura...
if exist .coverage del .coverage
if exist htmlcov rmdir /s /q htmlcov
if exist coverage.xml del coverage.xml

REM Tests unitarios
if %RUN_UNIT%==1 (
    echo [INFO] Ejecutando tests unitarios...
    if %WITH_COVERAGE%==1 (
        python -m pytest tests/unit/ -v --cov=. --cov-report=term-missing --cov-report=html --cov-config=.coveragerc
    ) else (
        python -m pytest tests/unit/ -v
    )
    if errorlevel 1 (
        echo [ERROR] Tests unitarios fallaron
        exit /b 1
    )
    echo [INFO] Tests unitarios completados
    echo.
)

REM Tests de integración
if %RUN_INTEGRATION%==1 (
    echo [INFO] Ejecutando tests de integracion...
    if %WITH_COVERAGE%==1 (
        python -m pytest tests/integration/ -v --cov=. --cov-append --cov-report=term-missing --cov-report=html --cov-config=.coveragerc
    ) else (
        python -m pytest tests/integration/ -v
    )
    if errorlevel 1 (
        echo [ERROR] Tests de integracion fallaron
        exit /b 1
    )
    echo [INFO] Tests de integracion completados
    echo.
)

REM Reporte de cobertura
if %WITH_COVERAGE%==1 (
    echo [INFO] Generando reporte de cobertura...
    python -m coverage report
    python -m coverage xml
    echo [INFO] Reporte HTML: htmlcov/index.html
    echo [INFO] Reporte XML: coverage.xml
)

echo.
echo ======================================
echo Todos los tests completados!
echo ======================================
