#!/usr/bin/env bash
# Render Start Script
# This script runs when starting the service on Render

set -o errexit  # Exit on error

echo "=== Starting Jitendra Portfolio API ==="
echo "PORT: ${PORT:-8000}"

# Start uvicorn server
# Use --workers for multiple worker processes in production
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
