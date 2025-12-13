#!/bin/bash
# CIEL GUI Client Launcher
# This script runs the GUI client with the correct Qt configuration

cd "$(dirname "$0")"
source venv/bin/activate

# Set environment variables for Qt to work in headless environments
export PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH
export QT_QPA_PLATFORM=minimal
export QT_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins

# Run the GUI client
python3 -m CLI
