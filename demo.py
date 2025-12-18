#!/usr/bin/env python3
"""
Demo script to showcase the Raspberry Pi Jukebox features
This script demonstrates the jukebox functionality without requiring audio files
"""

import time
from jukebox import Jukebox


def print_separator():
    print("\n" + "=" * 60)


def demo_jukebox():
    """Demonstrate jukebox features"""
    print("=" * 60)
    print("RASPBERRY PI JUKEBOX DEMO")
    print("=" * 60)
    print("\nThis demo showcases the jukebox features in simulation mode")
    print("(No audio files or pygame required)")
    
    # Create jukebox instance
    print("\n1. Creating Jukebox instance...")
    jukebox = Jukebox()
    time.sleep(1)
    
    # Create a mock playlist
    print_separator()
    print("2. Creating demo playlist...")
    jukebox.playlist = [
        "01-rock-song.mp3",
        "02-jazz-tune.mp3",
        "03-classical-piece.mp3",
        "04-electronic-beat.mp3",
        "05-folk-melody.mp3"
    ]
    print(f"   Loaded {len(jukebox.playlist)} tracks")
    time.sleep(1)
    
    # Display playlist
    print_separator()
    print("3. Displaying playlist...")
    jukebox.list_playlist()
    time.sleep(2)
    
    # Play first track
    print_separator()
    print("4. Playing first track...")
    jukebox.play(0)
    time.sleep(1)
    
    # Pause
    print_separator()
    print("5. Pausing playback...")
    jukebox.pause()
    time.sleep(1)
    
    # Resume
    print_separator()
    print("6. Resuming playback...")
    jukebox.resume()
    time.sleep(1)
    
    # Next track
    print_separator()
    print("7. Skipping to next track...")
    jukebox.next_track()
    time.sleep(1)
    
    # Enable shuffle
    print_separator()
    print("8. Enabling shuffle mode...")
    jukebox.toggle_shuffle()
    time.sleep(1)
    
    # Next track with shuffle
    print_separator()
    print("9. Playing next track (shuffled)...")
    jukebox.next_track()
    time.sleep(1)
    
    # Volume control
    print_separator()
    print("10. Adjusting volume...")
    jukebox.set_volume(0.8)
    time.sleep(0.5)
    jukebox.set_volume(0.5)
    time.sleep(0.5)
    jukebox.set_volume(0.7)
    time.sleep(1)
    
    # Previous track
    print_separator()
    print("11. Going to previous track...")
    jukebox.previous_track()
    time.sleep(1)
    
    # Enable repeat
    print_separator()
    print("12. Enabling repeat mode...")
    jukebox.toggle_repeat()
    time.sleep(1)
    
    # Get current track
    print_separator()
    print("13. Current track information...")
    current = jukebox.get_current_track()
    if current:
        print(f"   Currently playing: {current}")
        print(f"   Track index: {jukebox.current_index + 1}/{len(jukebox.playlist)}")
    time.sleep(1)
    
    # Stop playback
    print_separator()
    print("14. Stopping playback...")
    jukebox.stop()
    time.sleep(1)
    
    # Demo complete
    print_separator()
    print("DEMO COMPLETE!")
    print_separator()
    print("\nFeatures demonstrated:")
    print("  ✓ Playlist loading and management")
    print("  ✓ Play, pause, resume, stop controls")
    print("  ✓ Next/previous track navigation")
    print("  ✓ Shuffle mode")
    print("  ✓ Repeat mode")
    print("  ✓ Volume control")
    print("  ✓ Track information display")
    print("\nTo use with real audio files:")
    print("  1. Install pygame: pip3 install pygame")
    print("  2. Add music files to ./music/ directory")
    print("  3. Run: python3 jukebox.py")
    print_separator()


def demo_led_effects():
    """Demonstrate LED effects"""
    try:
        from led_control import LEDController
        
        print("\n\n")
        print("=" * 60)
        print("LED CONTROL DEMO")
        print("=" * 60)
        print("\nDemonstrating LED visual effects...")
        
        led = LEDController(enabled=True)
        
        # Test different colors
        print("\n1. Testing colors...")
        colors = ["red", "green", "blue", "yellow", "cyan", "magenta"]
        for color in colors:
            print(f"   Setting color: {color}")
            led.set_color(color)
            time.sleep(0.5)
        
        led.set_color("off")
        time.sleep(0.5)
        
        # Test brightness
        print("\n2. Testing brightness levels...")
        led.set_color("blue")
        for brightness in [0.25, 0.5, 0.75, 1.0]:
            print(f"   Brightness: {int(brightness * 100)}%")
            led.set_brightness(brightness)
            time.sleep(0.5)
        
        led.set_color("off")
        
        print("\n" + "=" * 60)
        print("LED Demo complete!")
        print("=" * 60)
        
        led.cleanup()
        
    except Exception as e:
        print(f"LED demo error: {e}")


if __name__ == "__main__":
    try:
        demo_jukebox()
        demo_led_effects()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nDemo error: {e}")
