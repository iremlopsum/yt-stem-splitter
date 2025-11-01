#!/bin/bash
# Integration test runner for the stems project
# These tests require network access and validate real YouTube URLs

echo "======================================================================"
echo "Running Integration Tests for Stems Project"
echo "======================================================================"
echo ""
echo "⚠️  NOTE: Integration tests require:"
echo "   - Network access"
echo "   - yt-dlp installed"
echo "   - Optional: essentia (for audio analysis)"
echo "   - Optional: selenium + undetected-chromedriver (for TuneBat)"
echo ""
echo "These tests validate real YouTube URLs:"
echo "   1. https://www.youtube.com/watch?v=33mjGmfy7PA"
echo "      Expected: BPM=99, Key=G Major"
echo ""
echo "   2. https://www.youtube.com/watch?v=AtNjDbxQZQI"
echo "      Expected: BPM=99, Key=A#min"
echo ""
echo "======================================================================"
echo ""

# Activate virtual environment if it exists
if [ -d "demucs-env" ]; then
    echo "Activating virtual environment..."
    source demucs-env/bin/activate
fi

# Run integration tests
if command -v pytest &> /dev/null; then
    echo "Running integration tests with pytest..."
    pytest tests/test_integration.py -v -s
else
    echo "pytest not found. Running with unittest..."
    python -m unittest tests.test_integration -v
fi

echo ""
echo "======================================================================"
echo "Integration Tests Complete"
echo "======================================================================"

