#!/bin/bash

echo "==========================================="
echo "   YouTube Playlist to MP3 Downloader      "
echo "==========================================="

# Detect Operating System to set correct executable paths and instructions
OS_TYPE=$(uname -s)
if [[ "$OS_TYPE" == *"MINGW"* ]] || [[ "$OS_TYPE" == *"CYGWIN"* ]] || [[ "$OS_TYPE" == *"MSYS"* ]]; then
    echo "Detected OS: Windows"
    PYTHON_CMD="python"
    VENV_DIR="yt_env/Scripts"
    FFMPEG_HELP="👉 Windows: Install via Winget (winget install ffmpeg) or download from https://www.gyan.dev/ffmpeg/builds/"
else
    if [[ "$OS_TYPE" == "Darwin" ]]; then
        echo "Detected OS: macOS"
        FFMPEG_HELP="👉 macOS: Install via Homebrew (brew install ffmpeg)"
    else
        echo "Detected OS: Linux"
        FFMPEG_HELP="👉 Linux: Install via your package manager (e.g., sudo apt install ffmpeg)"
    fi
    
    PYTHON_CMD="python3"
    VENV_DIR="yt_env/bin"
    
    # Fallback to 'python' if 'python3' command is not found
    if ! command -v python3 &> /dev/null; then
        PYTHON_CMD="python"
    fi
fi

# [0/4] Check for FFmpeg installation
echo "[0/4] Checking system requirements..."
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: FFmpeg is not installed or not in your PATH."
    echo "FFmpeg is strictly required to convert downloaded videos to MP3."
    echo "$FFMPEG_HELP"
    echo "Exiting..."
    exit 1
else
    echo "✅ FFmpeg is installed."
fi

# [1/4] Create virtual environment
echo "[1/4] Creating temporary virtual environment (yt_env)..."
$PYTHON_CMD -m venv yt_env

# [2/4] Install dependencies using the OS-specific pip path
echo "[2/4] Installing dependencies from requirements.txt..."
./$VENV_DIR/pip install --upgrade pip -q
./$VENV_DIR/pip install -r requirements.txt -q
echo "✅ Dependencies installed."

# [3/4] Run the downloader using the OS-specific python path
echo "[3/4] Starting downloader..."
echo "-------------------------------------------"
./$VENV_DIR/python playlist_downloader.py
echo "-------------------------------------------"

# [4/4] Cleanup
echo "Cleaning up..."
rm -rf yt_env
echo "✅ Temporary virtual environment (yt_env) deleted."
echo "🎉 Process complete!"