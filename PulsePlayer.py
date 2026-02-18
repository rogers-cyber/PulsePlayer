# ==========================================================
# PulsePlayer Music Player (Professional Architecture)
# ==========================================================

import sys
import os
import io
import time
import random
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from queue import Queue, Empty

import ttkbootstrap as tb
from ttkbootstrap.constants import *

from pathlib import Path

from PIL import Image, ImageTk, ImageDraw
from tinytag import TinyTag
import vlc
import numpy as np
from tkinterdnd2 import TkinterDnD

# ---------- OPTIONAL PYAUDIO ----------
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except:
    PYAUDIO_AVAILABLE = False

# ==========================================================
# CONFIG
# ==========================================================

APP_NAME = "PulsePlayer"
APP_VERSION = "1.0.1"
APP_AUTHOR = "Mate Technologies"
APP_WEBSITE = "https://matetools.gumroad.com"

SUPPORTED_AUDIO = (".mp3", ".wav", ".flac", ".m4a", ".ogg")

ROTATION_SPEED = 0.4
FPS_DELAY = 16
CROSSFADE_DURATION = 3

CHUNK = 1024
RATE = 44100

# ==========================================================
# UTILITIES
# ==========================================================

class AudioUtils:

    @staticmethod
    def format_time(sec):
        sec = int(sec)
        return f"{sec//60:02d}:{sec%60:02d}"

    @staticmethod
    def extract_album_art(path):
        try:
            tag = TinyTag.get(path, image=True)
            if tag.images and tag.images.front_cover:
                img = Image.open(io.BytesIO(tag.images.front_cover.data))
                img = img.resize((250, 250))
                return img
        except:
            pass
        return None

    @staticmethod
    def fetch_lyrics(path):
        try:
            tag = TinyTag.get(path)
            if hasattr(tag, "lyrics") and tag.lyrics:
                return tag.lyrics
        except:
            pass
        return "Lyrics not found."

    @staticmethod
    def is_valid_audio(path):
        return path.lower().endswith(SUPPORTED_AUDIO)

    @staticmethod
    def resource_path(name):
        base = getattr(sys, "_MEIPASS", Path(__file__).parent)
        return Path(base) / name
# ==========================================================
# PLAYLIST MANAGER
# ==========================================================

class PlaylistManager:
    def __init__(self):
        self.playlist = []

    def add_files(self, files):
        valid = [f for f in files if AudioUtils.is_valid_audio(f)]
        self.playlist.extend(valid)

    def filter(self, query):
        if not query:
            return self.playlist
        return [
            f for f in self.playlist
            if query.lower() in os.path.basename(f).lower()
        ]

# ==========================================================
# MUSIC PLAYER ENGINE (NO GUI HERE)
# ==========================================================

class MusicPlayerEngine:

    def __init__(self):
        self.vlc_instance = vlc.Instance("--no-video", "--quiet")
        self.player = self.vlc_instance.media_player_new()

        self.filtered_playlist = []
        self.current_index = -1

        self.loop_mode = False
        self.shuffle_mode = False
        self.is_paused = False

        self.loop_mode = False        # playlist loop
        self.single_loop = False      # single track loop


    def load_track(self, path):
        media = self.vlc_instance.media_new(path)
        self.player.set_media(media)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def set_volume(self, vol):
        self.player.audio_set_volume(vol)

    def get_length(self):
        """Return track length in seconds. Wait for VLC to parse if unknown."""
        length = self.player.get_length()  # in milliseconds
        if length <= 0:
            # Try parsing media
            media = self.player.get_media()
            if media:
                try:
                    media.parse_with_options(vlc.MediaParseFlag.parse_local, timeout=5)
                    length = media.get_duration()
                except:
                    length = 0
        return max(length / 1000, 0)  # return 0 if still unknown

    def get_time(self):
        return self.player.get_time() / 1000

    def seek(self, sec):
        self.player.set_time(int(sec * 1000))

    def is_playing(self):
        return self.player.is_playing()

    def next_index(self):
        if not self.filtered_playlist:
            return None

        if self.shuffle_mode:
            return random.randint(0, len(self.filtered_playlist) - 1)

        if self.single_loop:
            return self.current_index  # repeat the same track

        if self.current_index + 1 < len(self.filtered_playlist):
            return self.current_index + 1

        if self.loop_mode:  # playlist loop
            return 0

        return None

# ==========================================================
# AUDIO VISUALIZER
# ==========================================================

class AudioVisualizer:
    def __init__(self, canvas, num_bars=50):
        self.canvas = canvas
        self.num_bars = num_bars
        self.bars = []
        self.decay = 0.1
        self.current_heights = [0] * self.num_bars

        # Create bars
        self.bar_width = max(2, int(self.canvas.winfo_reqwidth() / self.num_bars))
        for i in range(self.num_bars):
            x0 = i * self.bar_width
            x1 = x0 + self.bar_width - 2
            bar = self.canvas.create_rectangle(x0, 100, x1, 100, fill="#1DB954")
            self.bars.append(bar)

    def update(self, root, engine):
        heights = []

        # Simulate bar heights based on playback position and some randomness
        if engine.is_playing():
            pos = engine.get_time()
            length = engine.get_length()
            progress = pos / max(length, 1)
            for i in range(self.num_bars):
                base = 20 + 60 * abs(np.sin(progress * 2 * np.pi + i / 5))
                noise = random.randint(-5, 5)
                heights.append(max(0, min(100, base + noise)))
        else:
            heights = [0] * self.num_bars

        # Smooth decay
        for i in range(self.num_bars):
            if heights[i] > self.current_heights[i]:
                self.current_heights[i] = heights[i]
            else:
                self.current_heights[i] -= self.decay * 100
                if self.current_heights[i] < 0:
                    self.current_heights[i] = 0

        # Update canvas bars with gradient
        for i, bar in enumerate(self.bars):
            x0, _, x1, _ = self.canvas.coords(bar)
            h = self.current_heights[i]

            if h < 33:
                color = "#1DB954"
            elif h < 66:
                color = "#FFC300"
            else:
                color = "#FF3D00"

            self.canvas.coords(bar, x0, 100, x1, 100 - h)
            self.canvas.itemconfig(bar, fill=color)

        # Schedule next frame
        root.after(30, lambda: self.update(root, engine))

# ==========================================================
# GUI APP
# ==========================================================

class SpotifyPlayerApp:

    def __init__(self):

        self.root = TkinterDnD.Tk()
        self.root.geometry("1200x680")
        self.root.title(APP_NAME)

        tb.Style("darkly")

        # Optional: set icon
        try:
            icon_path = AudioUtils.resource_path("logo.ico")

            if os.name == "nt":  # Windows
                self.root.iconbitmap(str(icon_path))
            else:
                img = ImageTk.PhotoImage(file=str(icon_path))
                self.root.iconphoto(True, img)

        except Exception as e:
            print("Icon error:", e)

        self.engine = MusicPlayerEngine()
        self.playlist_manager = PlaylistManager()

        self.progress_var = tk.DoubleVar()
        self.search_var = tk.StringVar()

        self.rotation_angle = 0
        self.album_original = None

        self._build_ui()
        self._create_menu()

    # --------------------------------------------------
    # UI BUILD
    # --------------------------------------------------

    def _build_ui(self):

        left = tb.Frame(self.root)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        right = tb.Frame(self.root)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # search
        search = tb.Entry(left, textvariable=self.search_var)
        search.pack(fill=tk.X)
        search.bind("<KeyRelease>", self.filter_playlist)

        # playlist
        self.listbox = tk.Listbox(left)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind("<Double-1>", self.play_selected)

        self.listbox.drop_target_register("DND_Files")
        self.listbox.dnd_bind("<<Drop>>", self.drop_files)

        # album art
        self.album_label = tk.Label(right)
        self.album_label.pack(pady=10)

        self.now_label = tb.Label(right, text="🎵 Now Playing")
        self.now_label.pack()

        self.duration_label = tb.Label(right, text="00:00 / 00:00")
        self.duration_label.pack()

        # progress
        self.progress_scale = tb.Scale(
            right,
            variable=self.progress_var,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL
        )
        self.progress_scale.pack(fill=tk.X)
        self.progress_scale.bind("<ButtonRelease-1>", self.seek)

        # controls
        controls = tb.Frame(right)
        controls.pack(pady=10)

        tb.Button(controls, text="⏮", command=self.prev_track).pack(side=tk.LEFT, padx=5)
        tb.Button(controls, text="▶", command=self.play_selected).pack(side=tk.LEFT, padx=5)
        tb.Button(controls, text="⏸", command=self.pause).pack(side=tk.LEFT, padx=5)
        tb.Button(controls, text="⏹", command=self.stop).pack(side=tk.LEFT, padx=5)
        tb.Button(controls, text="⏭", command=self.next_track).pack(side=tk.LEFT, padx=5)

        # Loop button: cycles between Off → Playlist → Single Track
        self.loop_modes = ["off", "playlist", "single"]
        self.loop_mode_index = 0
        self.loop_button = tb.Button(
            controls,
            text="🔁 Off",
            command=self.toggle_loop_mode
        )
        self.loop_button.pack(side=tk.LEFT, padx=5)

        # ----------------- VOLUME UP / DOWN -----------------
        self.volume_var = 80  # initial volume

        tb.Button(controls, text="🔉", command=self.volume_down).pack(side=tk.LEFT, padx=5)
        tb.Button(controls, text="🔊", command=self.volume_up).pack(side=tk.LEFT, padx=5)

        # Volume label
        self.volume_label = tb.Label(controls, text=f"Volume: {self.volume_var}")
        self.volume_label.pack(side=tk.LEFT, padx=5)

        # set initial volume
        self.engine.set_volume(self.volume_var)

        # lyrics
        self.lyrics = tk.Text(right, height=8, bg="#1e1e1e", fg="white")
        self.lyrics.pack(fill=tk.X, pady=10)

        # visualizer
        self.canvas = tk.Canvas(right, height=100, bg="#121212")
        self.canvas.pack(fill=tk.X)

        self.visualizer = AudioVisualizer(self.canvas, num_bars=50)  # or 60

    # ---------------- MENU ----------------

    def _create_menu(self):
        menubar = tk.Menu(self.root)  # <-- root, not self
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="Add Files", command=self.add_files)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)

    # --------------------------------------------------
    # PLAYBACK
    # --------------------------------------------------

    def play_selected(self, event=None):

        idx = self.listbox.curselection()
        if not idx:
            return

        self.engine.current_index = idx[0]
        file = self.engine.filtered_playlist[idx[0]]

        self.engine.load_track(file)
        self.engine.play()

        self.now_label.config(text=f"🎵 {os.path.basename(file)}")
        self._load_album_art(file)

        self.lyrics.delete("1.0", tk.END)
        self.lyrics.insert(tk.END, AudioUtils.fetch_lyrics(file))

        threading.Thread(target=self.update_progress_gui(), daemon=True).start()
        self.visualizer.update(self.root, self.engine)
        self.animate_album()

    def toggle_loop_mode(self):
        """Cycle through loop modes: Off → Playlist → Single Track"""
        self.loop_mode_index = (self.loop_mode_index + 1) % len(self.loop_modes)
        mode = self.loop_modes[self.loop_mode_index]

        self.engine.loop_mode = (mode == "playlist")
        self.engine.single_loop = (mode == "single")

        if mode == "off":
            self.loop_button.config(text="🔁 Off")
        elif mode == "playlist":
            self.loop_button.config(text="🔁 Playlist")
        else:
            self.loop_button.config(text="🔂 Single")

    def volume_up(self):
        """Increase volume by 5% and update label"""
        self.volume_var = min(100, self.volume_var + 5)
        self.engine.set_volume(self.volume_var)
        self.volume_label.config(text=f"Volume: {self.volume_var}")

    def volume_down(self):
        """Decrease volume by 5% and update label"""
        self.volume_var = max(0, self.volume_var - 5)
        self.engine.set_volume(self.volume_var)
        self.volume_label.config(text=f"Volume: {self.volume_var}")

    def set_volume(self, val):
        """Set VLC player volume from slider"""
        try:
            volume = int(float(val))  # slider passes string, convert to int
            self.engine.set_volume(volume)
        except Exception as e:
            print("Volume error:", e)

    def pause(self):
        self.engine.pause()

    def stop(self):
        self.engine.stop()

    def next_track(self):
        idx = self.engine.next_index()
        if idx is not None:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(idx)
            self.play_selected()

    def prev_track(self):
        if self.engine.current_index > 0:
            idx = self.engine.current_index - 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(idx)
            self.play_selected()

    # --------------------------------------------------
    # PROGRESS
    # --------------------------------------------------

    def update_progress_gui(self):
        if self.engine.current_index >= 0:
            length = self.engine.get_length()
            pos = self.engine.get_time()

            if length > 0:
                self.progress_scale.config(to=length)
                self.progress_var.set(pos)
                self.duration_label.config(
                    text=f"{AudioUtils.format_time(pos)} / {AudioUtils.format_time(length)}"
                )

                # ------------------ AUTO NEXT / LOOP ------------------
                if pos >= length - 0.5:  # end of track (small buffer)
                    next_idx = self.engine.next_index()
                    if next_idx is not None:
                        self.listbox.selection_clear(0, tk.END)
                        self.listbox.selection_set(next_idx)
                        self.play_selected()
                    else:
                        self.stop()  # no next track

        # schedule next update
        self.root.after(500, self.update_progress_gui)

    def seek(self, e):
        self.engine.seek(self.progress_var.get())

    # --------------------------------------------------
    # ALBUM ROTATION
    # --------------------------------------------------

    def _apply_circle_mask(self, img):
        """Return a circular masked version of img (PIL Image)"""
        size = img.size
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        result = img.copy()
        result.putalpha(mask)  # add transparency outside circle
        return result

    def _load_album_art(self, file):
        """Load album art as circular image"""
        img = AudioUtils.extract_album_art(file)
        if img:
            self.album_original = self._apply_circle_mask(img)
        else:
            placeholder = Image.new("RGB", (250, 250), color="#222222")
            self.album_original = self._apply_circle_mask(placeholder)
        
        self.album_photo = ImageTk.PhotoImage(self.album_original)
        self.album_label.config(image=self.album_photo)

    def animate_album(self):
        """Rotate circular album art"""
        if not self.album_original or not self.engine.is_playing():
            self.root.after(FPS_DELAY, self.animate_album)
            return

        self.rotation_angle = (self.rotation_angle + ROTATION_SPEED) % 360

        # Rotate while keeping alpha channel
        rotated = self.album_original.rotate(
            self.rotation_angle,
            resample=Image.BICUBIC,
            expand=False
        )

        self.album_photo = ImageTk.PhotoImage(rotated)
        self.album_label.config(image=self.album_photo)

        self.root.after(FPS_DELAY, self.animate_album)

    # --------------------------------------------------
    # PLAYLIST
    # --------------------------------------------------

    def refresh_playlist(self):
        self.listbox.delete(0, tk.END)
        for f in self.engine.filtered_playlist:
            self.listbox.insert(tk.END, os.path.basename(f))

    def add_files(self):
        files = filedialog.askopenfilenames()
        self.playlist_manager.add_files(files)
        self.engine.filtered_playlist = self.playlist_manager.playlist.copy()
        self.refresh_playlist()

    def drop_files(self, event):
        files = self.root.tk.splitlist(event.data)
        self.playlist_manager.add_files(files)
        self.engine.filtered_playlist = self.playlist_manager.playlist.copy()
        self.refresh_playlist()

    def filter_playlist(self, event=None):
        q = self.search_var.get()
        self.engine.filtered_playlist = self.playlist_manager.filter(q)
        self.refresh_playlist()

    # ---------------- ABOUT ----------------

    def _show_about(self):
        messagebox.showinfo(
            f"About {APP_NAME}",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "A professional Spotify-style music player built in Python.\n\n"
            "Features:\n"
            "• Crossfade playback\n"
            "• Smooth album art rotation\n"
            "• Playlist management & search\n"
            "• Lyrics display\n"
            "• Audio visualizer\n"
            "• Drag & Drop support\n\n"
            f"Developed by: {APP_AUTHOR}\n{APP_WEBSITE}"
        )

    # --------------------------------------------------

    def run(self):
        self.root.mainloop()

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    app = SpotifyPlayerApp()
    app.run()
