#!/bin/bash
# Test runner script for the stems project

echo "======================================"
echo "Running Unit Tests for Stems Project"
echo "======================================"
echo ""

# Activate virtual environment if it exists
if [ -d "demucs-env" ]; then
    echo "Activating virtual environment..."
    source demucs-env/bin/activate
fi

# Run tests with pytest if available, otherwise use unittest
if command -v pytest &> /dev/null; then
    echo "Running tests with pytest..."
    pytest tests/ -v --cov=src --cov-report=term-missing
else
    echo "pytest not found. Running tests with unittest..."
    python -m unittest discover -s tests -p "test_*.py" -v
fi

echo ""
echo "======================================"
echo "Tests Complete"
echo "======================================"

