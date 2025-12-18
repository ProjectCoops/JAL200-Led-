#!/usr/bin/env python3
"""
Raspberry Pi Jukebox Software
A simple music player with playlist management and LED control support
"""

import os
import json
import random
from pathlib import Path
from typing import List, Optional
import time

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame not available. Audio playback will be simulated.")


class Jukebox:
    """Main Jukebox class for managing music playback"""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize the jukebox with configuration"""
        self.config = self._load_config(config_path)
        self.playlist: List[str] = []
        self.current_index: int = 0
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.shuffle_mode: bool = False
        self.repeat_mode: bool = False
        
        if PYGAME_AVAILABLE:
            pygame.mixer.init()
        
        # Load initial playlist if specified
        if "default_playlist" in self.config:
            self.load_playlist(self.config["default_playlist"])
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {
            "music_dir": "./music",
            "volume": 0.7,
            "led_enabled": False
        }
    
    def load_playlist(self, playlist_path: str) -> bool:
        """Load a playlist from a file or directory"""
        if os.path.isdir(playlist_path):
            # Load all music files from directory
            self.playlist = self._scan_music_directory(playlist_path)
        elif os.path.isfile(playlist_path):
            # Load playlist file
            with open(playlist_path, 'r') as f:
                self.playlist = [line.strip() for line in f if line.strip()]
        else:
            print(f"Error: Playlist path not found: {playlist_path}")
            return False
        
        print(f"Loaded {len(self.playlist)} tracks")
        return True
    
    def _scan_music_directory(self, directory: str) -> List[str]:
        """Scan directory for music files"""
        music_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.m4a'}
        music_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if Path(file).suffix.lower() in music_extensions:
                    music_files.append(os.path.join(root, file))
        
        return sorted(music_files)
    
    def play(self, track_index: Optional[int] = None) -> bool:
        """Play a track from the playlist"""
        if not self.playlist:
            print("Error: No tracks in playlist")
            return False
        
        if track_index is not None:
            self.current_index = track_index % len(self.playlist)
        
        track = self.playlist[self.current_index]
        print(f"Playing: {os.path.basename(track)}")
        
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.load(track)
                pygame.mixer.music.set_volume(self.config.get("volume", 0.7))
                pygame.mixer.music.play()
                self.is_playing = True
                self.is_paused = False
                self._update_leds()
                return True
            except Exception as e:
                print(f"Error playing track: {e}")
                return False
        else:
            # Simulate playback
            self.is_playing = True
            self.is_paused = False
            self._update_leds()
            return True
    
    def pause(self):
        """Pause playback"""
        if PYGAME_AVAILABLE and self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            print("Paused")
            self._update_leds()
        elif not PYGAME_AVAILABLE and self.is_playing:
            self.is_paused = True
            print("Paused (simulated)")
            self._update_leds()
    
    def resume(self):
        """Resume playback"""
        if PYGAME_AVAILABLE and self.is_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            print("Resumed")
            self._update_leds()
        elif not PYGAME_AVAILABLE and self.is_paused:
            self.is_paused = False
            print("Resumed (simulated)")
            self._update_leds()
    
    def stop(self):
        """Stop playback"""
        if PYGAME_AVAILABLE and self.is_playing:
            pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        print("Stopped")
        self._update_leds()
    
    def next_track(self):
        """Play next track in playlist"""
        if not self.playlist:
            return
        
        if self.shuffle_mode:
            self.current_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.playlist)
        
        self.play()
    
    def previous_track(self):
        """Play previous track in playlist"""
        if not self.playlist:
            return
        
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()
    
    def toggle_shuffle(self):
        """Toggle shuffle mode"""
        self.shuffle_mode = not self.shuffle_mode
        print(f"Shuffle: {'ON' if self.shuffle_mode else 'OFF'}")
    
    def toggle_repeat(self):
        """Toggle repeat mode"""
        self.repeat_mode = not self.repeat_mode
        print(f"Repeat: {'ON' if self.repeat_mode else 'OFF'}")
    
    def set_volume(self, volume: float):
        """Set playback volume (0.0 to 1.0)"""
        volume = max(0.0, min(1.0, volume))
        self.config["volume"] = volume
        if PYGAME_AVAILABLE:
            pygame.mixer.music.set_volume(volume)
        print(f"Volume: {int(volume * 100)}%")
    
    def get_current_track(self) -> Optional[str]:
        """Get currently playing track"""
        if self.playlist and 0 <= self.current_index < len(self.playlist):
            return self.playlist[self.current_index]
        return None
    
    def list_playlist(self):
        """Display current playlist"""
        if not self.playlist:
            print("Playlist is empty")
            return
        
        print(f"\n=== Playlist ({len(self.playlist)} tracks) ===")
        for i, track in enumerate(self.playlist):
            marker = "▶ " if i == self.current_index else "  "
            print(f"{marker}{i+1}. {os.path.basename(track)}")
        print()
    
    def _update_leds(self):
        """Update LED status based on playback state"""
        if not self.config.get("led_enabled", False):
            return
        
        # LED control logic for JAL200 LEDs
        # This is a placeholder - actual implementation depends on hardware
        try:
            if self.is_playing and not self.is_paused:
                # Green LED for playing
                self._set_led_color("green")
            elif self.is_paused:
                # Yellow LED for paused
                self._set_led_color("yellow")
            else:
                # Red LED for stopped
                self._set_led_color("red")
        except Exception as e:
            print(f"LED update error: {e}")
    
    def _set_led_color(self, color: str):
        """Set LED color (placeholder for actual hardware control)"""
        # This would interface with actual LED hardware
        # For now, just log the action
        pass


def main():
    """Main entry point for the jukebox application"""
    import sys
    
    print("=" * 50)
    print("Raspberry Pi Jukebox")
    print("=" * 50)
    
    jukebox = Jukebox()
    
    # Command line argument handling
    if len(sys.argv) > 1:
        if sys.argv[1] == "--load" and len(sys.argv) > 2:
            jukebox.load_playlist(sys.argv[2])
    
    # Interactive mode
    print("\nCommands:")
    print("  play [n] - Play track n (or current track)")
    print("  pause    - Pause playback")
    print("  resume   - Resume playback")
    print("  stop     - Stop playback")
    print("  next     - Next track")
    print("  prev     - Previous track")
    print("  shuffle  - Toggle shuffle mode")
    print("  repeat   - Toggle repeat mode")
    print("  volume n - Set volume (0-100)")
    print("  list     - Show playlist")
    print("  load p   - Load playlist from path")
    print("  quit     - Exit jukebox")
    print()
    
    while True:
        try:
            cmd = input("jukebox> ").strip().split()
            if not cmd:
                continue
            
            command = cmd[0].lower()
            
            if command == "quit" or command == "exit":
                jukebox.stop()
                print("Goodbye!")
                break
            elif command == "play":
                if len(cmd) > 1 and cmd[1].isdigit():
                    jukebox.play(int(cmd[1]) - 1)
                else:
                    jukebox.play()
            elif command == "pause":
                jukebox.pause()
            elif command == "resume":
                jukebox.resume()
            elif command == "stop":
                jukebox.stop()
            elif command == "next":
                jukebox.next_track()
            elif command == "prev" or command == "previous":
                jukebox.previous_track()
            elif command == "shuffle":
                jukebox.toggle_shuffle()
            elif command == "repeat":
                jukebox.toggle_repeat()
            elif command == "volume" and len(cmd) > 1:
                try:
                    vol = int(cmd[1]) / 100.0
                    jukebox.set_volume(vol)
                except ValueError:
                    print("Invalid volume value")
            elif command == "list":
                jukebox.list_playlist()
            elif command == "load" and len(cmd) > 1:
                jukebox.load_playlist(cmd[1])
            elif command == "help":
                print("\nCommands: play, pause, resume, stop, next, prev, shuffle, repeat, volume, list, load, quit")
            else:
                print("Unknown command. Type 'help' for commands.")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            jukebox.stop()
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
