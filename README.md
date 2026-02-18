# PulsePlayer v1.0.1 – Professional Spotify-Style Music Player (Source Code + EXE)

PulsePlayer v1.0.1 is a professional desktop music player built with Python and VLC.  
It features a modern Spotify-style interface, smooth album art animation, playlist management, lyrics display, audio visualization, and advanced playback controls.

The application is designed for performance, simplicity, and a premium user experience with drag & drop support and real-time playback updates.

This repository includes:
- Full Python source code
- Prebuilt Windows executable available under the Releases section
- Portable desktop music player for personal and professional use

------------------------------------------------------------
WINDOWS DOWNLOAD (EXE)
------------------------------------------------------------

Download the latest Windows executable from GitHub Releases:

https://github.com/yourusername/PulsePlayer/releases

- No Python required
- Portable executable
- Ready-to-run on Windows

------------------------------------------------------------
FEATURES
------------------------------------------------------------

- Spotify-Style Modern UI
- High-performance audio playback using VLC engine
- Smooth circular album art rotation
- Real-time playback progress tracking
- Playlist management with search filter
- Drag & Drop file support
- Lyrics display from audio metadata
- Dynamic audio visualizer
- Loop modes:
  - Off
  - Playlist Loop
  - Single Track Repeat
- Shuffle playback support
- Volume controls with live update
- Time seek bar with position control
- Automatic track transition
- Threaded background updates for responsive UI
- Fully offline playback (no internet required)
- Cross-platform Python source
- Modern interface powered by ttkbootstrap

------------------------------------------------------------
SUPPORTED AUDIO FORMATS
------------------------------------------------------------

- MP3 (.mp3)
- WAV (.wav)
- FLAC (.flac)
- M4A (.m4a)
- OGG (.ogg)

------------------------------------------------------------
REPOSITORY STRUCTURE
------------------------------------------------------------

PulsePlayer/
├── PulsePlayer.py
├── dist/
│   └── (empty or .gitkeep)
├── logo.ico
├── requirements.txt
├── README.md
└── LICENSE

------------------------------------------------------------
INSTALLATION (SOURCE CODE)
------------------------------------------------------------

1. Clone the repository:

```
git clone https://github.com/rogers-cyber/PulsePlayer.git
cd PulsePlayer
```

2. Install dependencies:

```
pip install -r requirements.txt
```

(Tkinter is included with standard Python installations.)

3. Run the application:

```
python PulsePlayer.py
```

------------------------------------------------------------
HOW TO USE
------------------------------------------------------------

1. **Add Music Files**
   - Use "Add Files" from menu
   - Or drag & drop audio files into the playlist

2. **Play Music**
   - Double-click any track
   - Use playback controls (Play / Pause / Stop / Next / Previous)

3. **Control Playback**
   - Seek using progress bar
   - Adjust volume using controls
   - Enable loop or repeat modes

4. **Search Music**
   - Use the search box to filter playlist items

5. **View Lyrics**
   - Lyrics appear automatically if embedded in audio metadata

6. **Visual Experience**
   - Watch rotating album artwork
   - View dynamic audio visualizer during playback

------------------------------------------------------------
DEPENDENCIES
------------------------------------------------------------

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
NOTES
------------------------------------------------------------

- VLC must be installed on your system or accessible via PATH
- Album artwork is extracted from audio metadata when available
- Lyrics are read from embedded metadata
- Visualizer currently simulates audio activity
- Performance depends on system audio and disk speed
- Crossfade functionality reserved for future versions

------------------------------------------------------------
ABOUT
------------------------------------------------------------

PulsePlayer is a lightweight, professional desktop music player designed to provide a modern listening experience with powerful playback features and a clean interface.

It is suitable for:
- Music enthusiasts
- Developers learning media playback systems
- Desktop application users
- Audio collection management
- Offline music playback workflows

------------------------------------------------------------
LICENSE
------------------------------------------------------------

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software,  
including the source code and compiled executable, with attribution.

See the LICENSE file for full details.
