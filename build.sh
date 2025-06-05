#!/bin/bash

# Exit on error
set -e

echo "Removing old venv_build directory..."
rm -rf "venv_build" # Quoted to be safe with VENV_NAME variable later if used

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
echo "Creating virtual environment: $VENV_NAME"
python3 -m venv "$VENV_NAME"

echo "Activating virtual environment..."
source "$VENV_NAME/bin/activate"

# --- Install/Upgrade Build Tools and Dependencies ---
echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Nuitka, setuptools, and wheel..."
pip install --no-cache-dir nuitka setuptools wheel

echo "Installing NumPy (no cache)..."
pip install --no-cache-dir numpy

echo "Installing freetype-py (no cache)..."
pip install --no-cache-dir freetype-py

echo "Installing remaining dependencies from requirements.txt (no cache)..."
pip install --no-cache-dir -r requirements.txt

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
    "--include-module=freetype"
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
