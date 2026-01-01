#!/bin/bash
# This script installs Playwright browsers and dependencies on Heroku

echo "Installing Playwright dependencies..."

# Install Playwright browsers
python -m playwright install chromium

# Install system dependencies for Chromium
echo "System dependencies will be installed via Aptfile"

echo "Playwright setup complete!"
