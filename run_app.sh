#!/bin/bash
# Unix/Mac Startup Script for Employee Performance Evaluation System

echo "========================================"
echo "Starting Health Check..."
echo "========================================"
python health_check.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Health check failed. Fix issues and try again."
    exit 1
fi

echo ""
echo "========================================"
echo "Launching Streamlit Application..."
echo "========================================"
streamlit run main.py
