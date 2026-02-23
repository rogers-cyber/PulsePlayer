# PulsePlayer v1.0.2 – Professional Spotify-Style Music Player (Source Code + EXE)

PulsePlayer v1.0.2 is a professional desktop music player built with Python and VLC.  
It features a modern Spotify-style interface, smooth album art animation, persistent playlist storage, session resume capability, lyrics display, audio visualization, and advanced playback controls.

The application is designed for performance, simplicity, and a premium user experience with drag & drop support, automatic session saving, and real-time playback updates.

This repository includes:

- Full Python source code
- Prebuilt Windows executable available under the Releases section
- Portable desktop music player for personal and professional use

------------------------------------------------------------

## WINDOWS DOWNLOAD (EXE)

Download the latest Windows executable from GitHub Releases:

https://github.com/rogers-cyber/PulsePlayer/releases

- No Python required
- Portable executable
- Ready-to-run on Windows

------------------------------------------------------------

## FEATURES

### 🎵 Core Playback
- Spotify-Style Modern UI
- High-performance audio playback using VLC engine
- Fully offline playback (no internet required)
- Automatic track transition
- Time seek bar with position control
- Volume controls with live update
- Threaded background updates for responsive UI

### 🎧 Playlist Management
- Persistent playlist storage (auto-saved)
- Playlist search filter
- Drag & Drop file support
- Clear entire playlist option
- Automatic playlist loading on startup

### 🔁 Advanced Playback Controls
- Loop modes:
  - Off
  - Playlist Loop
  - Single Track Repeat
- Shuffle playback support
- Resume last played track automatically
- Resume exact playback position after restart

### 🎨 Visual Experience
- Smooth circular album art rotation
- Real-time playback progress tracking
- Dynamic audio visualizer
- Lyrics display from audio metadata

### ⚡ Professional Architecture
- Modular player engine (GUI separated from playback logic)
- Cross-platform Python source
- Modern interface powered by ttkbootstrap
- Lightweight and high-performance design

------------------------------------------------------------

## SUPPORTED AUDIO FORMATS

- MP3 (.mp3)
- WAV (.wav)
- FLAC (.flac)
- M4A (.m4a)
- OGG (.ogg)

------------------------------------------------------------

## REPOSITORY STRUCTURE

PulsePlayer/  
├── PulsePlayer.py  
├── dist/  
│   └── (empty or .gitkeep)  
├── logo.ico  
├── requirements.txt  
├── README.md  
└── LICENSE  

------------------------------------------------------------

## INSTALLATION (SOURCE CODE)

### 1. Clone the repository

git clone https://github.com/rogers-cyber/PulsePlayer.git  
cd PulsePlayer

### 2. Install dependencies

pip install -r requirements.txt

(Tkinter is included with standard Python installations.)

### 3. Run the application

python PulsePlayer.py

------------------------------------------------------------

## HOW TO USE

### 1. Add Music Files
- Use **Add Files** from menu
- Or drag & drop audio files into the playlist

### 2. Play Music
- Double-click any track
- Use playback controls (Play / Pause / Stop / Next / Previous)

### 3. Control Playback
- Seek using progress bar
- Adjust volume using controls
- Enable loop or repeat modes
- Resume playback automatically after restarting the app

### 4. Manage Playlist
- Use search box to filter tracks
- Clear all tracks using **Clear All Music**
- Playlist saves automatically

### 5. View Lyrics
- Lyrics appear automatically if embedded in audio metadata

### 6. Visual Experience
- Watch rotating album artwork
- View dynamic audio visualizer during playback

------------------------------------------------------------

## DEPENDENCIES

- Python 3.9+
- ttkbootstrap
- python-vlc
- Pillow
- tinytag
- numpy
- tkinterdnd2
- pyaudio (optional for future audio processing features)
- threading / os / sys / io / random / pathlib / queue (standard Python libraries)

See requirements.txt for exact versions.

------------------------------------------------------------

## NOTES

- VLC must be installed on your system or accessible via PATH
- Playlist and session state are automatically saved locally
- Album artwork is extracted from audio metadata when available
- Lyrics are read from embedded metadata
- Visualizer currently simulates audio activity
- Performance depends on system audio and disk speed
- Crossfade functionality reserved for future versions

------------------------------------------------------------

## ABOUT

PulsePlayer is a lightweight, professional desktop music player designed to provide a modern listening experience with powerful playback features and a clean interface.

It is suitable for:

- Music enthusiasts
- Developers learning media playback systems
- Desktop application users
- Audio collection management
- Offline music playback workflows

------------------------------------------------------------

## LICENSE

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software,  
including the source code and compiled executable, with attribution.


See the LICENSE file for full details.
