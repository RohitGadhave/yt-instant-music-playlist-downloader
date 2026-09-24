# YouTube Playlist to MP3 Downloader

A lightweight, automated tool to download legally permitted YouTube playlists and convert them to MP3 format. It runs in an isolated, temporary virtual environment so no extra space is permanently consumed by Python packages on your system.

## Prerequisites

1. **Python 3**: Ensure Python 3 is installed on your system.
2. **FFmpeg**: This is required for the MP3 conversion.
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg`
   - **Windows:** Use winget (`winget install ffmpeg`)

## Files Included

- `setup_and_run.sh`: The main execution script. It automates environment creation, package installation, running the tool, and cleanup.
- `playlist_downloader.py`: The core Python logic using `yt-dlp`.
- `requirements.txt`: Lists the Python dependencies.
- `README.md`: This documentation file.

## How to Use (macOS/Linux)

1. Open your terminal and navigate to the directory containing these files.
2. Make the bash script executable (you only need to do this once):
   ```bash
   chmod +x setup_and_run.sh
   ```
3. Run the script:
   ```bash
   ./setup_and_run.sh
   ```
4. Paste your playlist URL when prompted.

## How it Works

When you run `setup_and_run.sh`, the script will:
1. Create a temporary Python virtual environment (`yt_env`).
2. Activate it and silently install `yt-dlp`.
3. Prompt you for the playlist URL and download the tracks into a newly created folder.
4. Automatically delete the `yt_env` folder when finished to save system space.