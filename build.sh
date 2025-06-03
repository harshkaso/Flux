#!/bin/bash

# Exit on error
set -e

# --- Configuration ---
APP_NAME="Flux"
ENTRY_POINT="flux/__main__.py"
VENV_NAME="venv_build"
DIST_DIR="dist"

# --- OS Detection ---
OS_NAME=$(uname -s)
OUTPUT_NAME="${APP_NAME}_${OS_NAME}"

if [ "$OS_NAME" = "Darwin" ]; then
    OS_NAME="macOS"
    OUTPUT_NAME="${APP_NAME}_macOS"
elif [ "$OS_NAME" = "Linux" ]; then
    OUTPUT_NAME="${APP_NAME}_Linux"
else
    echo "Unsupported OS: $OS_NAME"
    exit 1
fi

echo "Building for $OS_NAME, output name: $OUTPUT_NAME"

# --- Setup Virtual Environment ---
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating virtual environment: $VENV_NAME"
    python3 -m venv "$VENV_NAME"
else
    echo "Virtual environment $VENV_NAME already exists."
fi

echo "Activating virtual environment..."
source "$VENV_NAME/bin/activate"

# --- Install/Upgrade Build Tools and Dependencies ---
echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Nuitka, setuptools, and wheel..."
pip install nuitka setuptools wheel

echo "Installing NumPy first (if required as a build-time dependency for other packages)..."
pip install numpy

echo "Installing remaining dependencies from requirements.txt..."
pip install -r requirements.txt

# --- Create Distribution Directory ---
mkdir -p "$DIST_DIR"

# --- Run Nuitka ---
echo "Running Nuitka to build the executable..."

# Nuitka options
NUITKA_OPTIONS=(
    "--onefile"
    "--output-dir=$DIST_DIR"
    "--output-filename=$OUTPUT_NAME"
    "--enable-plugin=numpy"
    # Data files and directories
    "--include-data-dir=assets=assets"
    "--include-data-dir=flux/Space_Mono=flux/Space_Mono"
    # Add more options as needed
    # "--enable-plugin=tk-inter" # If dearpygui has issues with tkinter backend
    # For macOS, if using entitlements:
    # "--macos-app-entitlements=path/to/your.entitlements"
)

echo "Nuitka command: python -m nuitka ${NUITKA_OPTIONS[@]} $ENTRY_POINT"
python -m nuitka "${NUITKA_OPTIONS[@]}" "$ENTRY_POINT"

echo "Build process completed."
echo "Executable should be in $DIST_DIR/$OUTPUT_NAME"

# --- Deactivate Virtual Environment (optional) ---
# echo "Deactivating virtual environment."
# deactivate

exit 0
