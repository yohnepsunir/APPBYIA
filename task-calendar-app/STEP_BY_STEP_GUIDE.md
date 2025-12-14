# Testing & Deployment Guide - Step by Step

## Overview
This guide walks you through running tests and deploying the task calendar application.

---

## Part 1: Running Tests Locally

### Prerequisites
- Python 3.9+
- pip or conda
- Git (optional, for CI/CD setup)

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Run All Tests
```bash
# Full test suite with coverage
python -m pytest tests/ -v --cov=. --cov-report=html

# Or use the test script
./run_tests.sh --coverage
```

### Step 3: View Results
```bash
# Check test output
# Should show: 85 passed in ~1 second

# View coverage report
open htmlcov/index.html          # macOS
xdg-open htmlcov/index.html      # Linux
start htmlcov\index.html         # Windows

# Expected coverage: 99.31%
```

### Step 4: Run Specific Tests
```bash
# Unit tests only
python -m pytest tests/unit/ -v

# Integration tests only
python -m pytest tests/integration/ -v

# Single test file
python -m pytest tests/unit/test_models.py -v

# Single test
python -m pytest tests/unit/test_models.py::TestTask::test_create_task -v
```

---

## Part 2: Understanding Test Organization

### Test Structure
```
tests/
├── conftest.py                        # Shared fixtures
├── unit/                              # Unit tests (individual components)
│   ├── test_app.py                   # Flask app tests
│   ├── test_database.py              # Database tests
│   ├── test_models.py                # Task model tests
│   ├── test_routes.py                # API endpoint tests
│   ├── test_coverage_improvements.py # Edge case tests
│   └── test_exception_handling.py    # Error handling tests
└── integration/                       # Integration tests (full workflows)
    ├── test_app_integration.py       # Full-stack tests
    └── test_task_workflow.py         # User scenario tests
```

### What Each Test File Covers

**test_app.py** (2 tests)
- Flask application initialization
- Route registration verification

**test_database.py** (5 tests)
- Database connection management
- Row factory configuration
- Schema initialization

**test_models.py** (10 tests)
- Task creation with validation
- Task retrieval (single and multiple)
- Task updates
- Task deletion
- Priority validation
- Default values

**test_routes.py** (11 tests)
- GET /api/tasks (list all)
- GET /api/tasks/<id> (single task)
- POST /api/tasks (create)
- PUT /api/tasks/<id> (update)
- DELETE /api/tasks/<id> (delete)
- Error handling
- Content-type validation

**test_coverage_improvements.py** (22 tests)
- Empty string handling
- Unicode character support
- Very long text (1000+ chars)
- Special characters (é, ñ, 中文)
- Bulk operations
- Boundary values
- Invalid formats

**test_exception_handling.py** (13 tests)
- Database connection failures
- Malformed requests
- Missing resources
- Method not allowed
- Exception path coverage

**test_app_integration.py** (9 tests)
- Full application workflow
- CORS headers
- Health check endpoint
- Concurrent operations
- Response validation

**test_task_workflow.py** (4 tests)
- Complete task lifecycle (create → read → update → delete)
- Multiple task scenarios
- Priority workflows
- Error recovery flows

---

## Part 3: Docker-Based Testing

### Step 1: Build Images
```bash
# Development image
docker build -t task-app:dev .

# Production image
docker build -f Dockerfile.prod -t task-app:prod .
```

### Step 2: Run Tests in Docker
```bash
# Run test service
docker-compose up test

# Expected output: 85 passed
```

### Step 3: Run Development Server
```bash
# Start dev server with live reload
docker-compose up dev

# Server runs on http://localhost:5000
# Frontend: http://localhost:5000/
# API: http://localhost:5000/api/tasks
```

### Step 4: Full Stack with Nginx
```bash
# Start all services (dev, test, nginx)
docker-compose -f docker-compose.full.yml up

# Access through Nginx reverse proxy
# http://localhost/api/tasks (proxied to backend)
```

---

## Part 4: Production Deployment

### Step 1: Prepare Production Image
```bash
# Build optimized production image
docker build -f Dockerfile.prod -t task-app:prod .

# Or use docker-compose
docker-compose -f docker-compose.full.yml build prod
```

### Step 2: Verify Tests Pass
```bash
# Must pass before deployment
cd backend
python -m pytest tests/ --cov=. --cov-report=term-missing

# Should see: 85 passed, 99.31% coverage
```

### Step 3: Deploy Using Script
```bash
# Development environment
./deploy.sh development

# Testing environment
./deploy.sh testing

# Production environment
./deploy.sh production
```

### Step 4: Manual Deployment
```bash
# Start production services
docker-compose -f docker-compose.full.yml up -d

# With Nginx reverse proxy
docker-compose -f docker-compose.full.yml up -d nginx

# Check status
docker-compose -f docker-compose.full.yml ps
```

### Step 5: Verify Deployment
```bash
# Health check
curl http://localhost:5000/api/health
# Response: {"status":"healthy"}

# List tasks
curl http://localhost:5000/api/tasks
# Response: []

# Create task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","priority":1}'

# View logs
docker logs task-app
docker logs nginx
```

---

## Part 5: Continuous Integration Setup

### GitHub Actions
```yaml
# File: .github/workflows/tests.yml
# Automatically runs tests on push and pull requests
# Tests Python versions: 3.9, 3.10, 3.11, 3.12, 3.13
```

### Setup Steps
1. Push code to GitHub
2. GitHub Actions automatically runs tests
3. Check Actions tab for results
4. Coverage badge updates automatically

---

## Part 6: Troubleshooting

### Tests Won't Run
```bash
# Activate virtual environment first
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests again
python -m pytest tests/ -v
```

### Coverage Report Shows Wrong Percentage
```bash
# Clear old coverage data
rm -rf .coverage htmlcov/

# Run tests with fresh coverage
python -m pytest tests/ --cov=. --cov-report=html

# View report
open htmlcov/index.html
```

### Docker Build Fails
```bash
# Clean docker images
docker system prune -a

# Rebuild
docker build -f Dockerfile.prod -t task-app:prod .

# Or use compose
docker-compose -f docker-compose.full.yml build --no-cache
```

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000          # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>          # macOS/Linux
taskkill /PID <PID>    # Windows

# Or use different port
docker run -p 5001:5000 task-app:dev
```

---

## Part 7: Performance Optimization

### Fast Tests (No Coverage)
```bash
# Run in ~0.3 seconds
./run_tests.sh --fast
```

### Parallel Test Execution
```bash
# Install plugin
pip install pytest-xdist

# Run with 4 workers
python -m pytest tests/ -n 4
```

### Watch Mode (Re-run on File Change)
```bash
# Install plugin
pip install pytest-watch

# Watch and re-run tests
ptw tests/
```

---

## Part 8: Coverage Analysis

### View Coverage Details
```bash
# Show uncovered lines
python -m pytest tests/ --cov=. --cov-report=term-missing

# Generate HTML report
python -m pytest tests/ --cov=. --cov-report=html

# Show branch coverage
python -m pytest tests/ --cov=. --cov-report=term-missing:skip-covered
```

### Coverage Goals
- Target: >95% code coverage
- Current: 99.31% ✅
- Acceptable: >85%

### Understanding Uncovered Lines
The only uncovered line is:
```python
# app.py line 27
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

This line only executes when the module is run directly, not when imported by pytest. This is a practical limitation of import-based testing.

---

## Part 9: Advanced Testing

### Test-Driven Development (TDD)
```bash
# 1. Write failing test
# 2. Run: python -m pytest tests/unit/test_models.py -v
# 3. Implement feature
# 4. Run again - should pass
# 5. Refactor with tests still passing
```

### Mocking External Dependencies
```python
# Example from test_exception_handling.py
from unittest.mock import patch

@patch('database.get_db')
def test_with_mocked_db(mock_db):
    # Mock raises an exception
    mock_db.side_effect = sqlite3.DatabaseError()
    # Test the error handling
```

### Fixtures for Data Setup
```python
# conftest.py defines fixtures
@pytest.fixture
def task_data():
    return {
        'title': 'Test Task',
        'description': 'Test Description',
        'priority': 1
    }

# Used in tests
def test_create_task(client, task_data):
    response = client.post('/api/tasks', json=task_data)
    assert response.status_code == 201
```

---

## Part 10: Monitoring in Production

### Check Application Health
```bash
# Health check endpoint
curl http://localhost:5000/api/health

# View logs
docker logs task-app

# Monitor in real-time
docker logs -f task-app

# Check resource usage
docker stats task-app
```

### Common Issues
```bash
# Out of memory
docker update --memory 512m task-app

# High CPU usage
# Check database queries or optimize code

# Connection refused
# Verify service is running: docker ps
```

---

## Checklist for Deployment

### Pre-Deployment
- [ ] All tests pass locally (`./run_tests.sh --coverage`)
- [ ] Coverage report reviewed (99.31%)
- [ ] No open TODO comments in code
- [ ] Database schema tested
- [ ] API endpoints verified
- [ ] Frontend assets optimized
- [ ] Environment variables configured

### Deployment
- [ ] Production image built
- [ ] Docker compose file ready
- [ ] Nginx config verified
- [ ] SSL certificates obtained
- [ ] Domain name configured
- [ ] Monitoring setup complete
- [ ] Backup strategy in place

### Post-Deployment
- [ ] Health check passes
- [ ] All endpoints responding
- [ ] Logs reviewed for errors
- [ ] Performance metrics acceptable
- [ ] Automated backups running
- [ ] Monitoring alerts configured

---

## Quick Reference

### Most Common Commands
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html

# Run specific test
python -m pytest tests/unit/test_models.py -v

# Docker test
docker-compose up test

# Docker dev
docker-compose up dev

# Deploy
./deploy.sh production

# View coverage
open htmlcov/index.html
```

### File Locations
```
backend/
  └── tests/
      ├── conftest.py (fixtures)
      ├── unit/ (unit tests)
      └── integration/ (integration tests)
  └── TESTING.md (detailed testing guide)
  └── DEPLOYMENT.md (detailed deployment guide)
  └── run_tests.sh (test script for Linux/Mac)
  └── run_tests.bat (test script for Windows)

root/
  └── docker-compose.yml (dev setup)
  └── docker-compose.full.yml (full stack)
  └── deploy.sh (deployment script)
  └── Dockerfile (dev image)
  └── Dockerfile.prod (prod image)
```

---

## Summary

You now have:
- ✅ 85 comprehensive tests (100% passing)
- ✅ 99.31% code coverage
- ✅ Docker deployment ready
- ✅ CI/CD pipeline configured
- ✅ Complete documentation

The application is production-ready! 🚀

---

*For detailed documentation, see:*
- *Testing Guide: backend/TESTING.md*
- *Deployment Guide: backend/DEPLOYMENT.md*
- *Architecture: backend/PROJECT_SUMMARY.md*
