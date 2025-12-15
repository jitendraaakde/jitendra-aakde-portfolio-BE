#!/usr/bin/env bash
# Render Build Script
# This script runs during the build phase on Render

set -o errexit  # Exit on error

echo "=== Starting Render Build ==="

# Upgrade pip to latest version
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "=== Build Complete ==="
