#!/usr/bin/env python3
"""
Simple test script for Jukebox functionality
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jukebox import Jukebox
from led_control import LEDController


def test_jukebox_initialization():
    """Test jukebox initialization"""
    print("Testing jukebox initialization...")
    jukebox = Jukebox()
    assert jukebox is not None
    assert jukebox.playlist == []
    assert jukebox.current_index == 0
    assert jukebox.is_playing == False
    print("✓ Jukebox initialization successful")


def test_playlist_operations():
    """Test playlist operations"""
    print("\nTesting playlist operations...")
    jukebox = Jukebox()
    
    # Test with empty playlist
    assert len(jukebox.playlist) == 0
    
    # Test loading non-existent playlist
    result = jukebox.load_playlist("/nonexistent/path")
    assert result == False
    
    print("✓ Playlist operations working correctly")


def test_playback_controls():
    """Test playback control methods"""
    print("\nTesting playback controls...")
    jukebox = Jukebox()
    
    # Create a test playlist with dummy files
    jukebox.playlist = ["song1.mp3", "song2.mp3", "song3.mp3"]
    
    # Test navigation
    jukebox.current_index = 0
    jukebox.next_track()
    assert jukebox.current_index == 1
    
    jukebox.previous_track()
    assert jukebox.current_index == 0
    
    # Test wrap-around
    jukebox.current_index = 2
    jukebox.next_track()
    assert jukebox.current_index == 0
    
    print("✓ Playback controls working correctly")


def test_shuffle_and_repeat():
    """Test shuffle and repeat modes"""
    print("\nTesting shuffle and repeat modes...")
    jukebox = Jukebox()
    
    # Test shuffle toggle
    assert jukebox.shuffle_mode == False
    jukebox.toggle_shuffle()
    assert jukebox.shuffle_mode == True
    jukebox.toggle_shuffle()
    assert jukebox.shuffle_mode == False
    
    # Test repeat toggle
    assert jukebox.repeat_mode == False
    jukebox.toggle_repeat()
    assert jukebox.repeat_mode == True
    jukebox.toggle_repeat()
    assert jukebox.repeat_mode == False
    
    print("✓ Shuffle and repeat modes working correctly")


def test_volume_control():
    """Test volume control"""
    print("\nTesting volume control...")
    jukebox = Jukebox()
    
    # Test volume setting
    jukebox.set_volume(0.5)
    assert jukebox.config["volume"] == 0.5
    
    # Test volume bounds
    jukebox.set_volume(1.5)  # Should be clamped to 1.0
    assert jukebox.config["volume"] == 1.0
    
    jukebox.set_volume(-0.5)  # Should be clamped to 0.0
    assert jukebox.config["volume"] == 0.0
    
    print("✓ Volume control working correctly")


def test_led_controller():
    """Test LED controller"""
    print("\nTesting LED controller...")
    led = LEDController(enabled=False)
    
    assert led is not None
    assert led.enabled == False
    assert led.current_color == "off"
    
    # Test color setting (should work even when disabled)
    led.set_color("red")
    led.set_color("green")
    led.set_color("off")
    
    print("✓ LED controller working correctly")


def test_led_brightness():
    """Test LED brightness control"""
    print("\nTesting LED brightness...")
    led = LEDController(enabled=False)
    
    # Test brightness setting
    led.set_brightness(0.5)
    assert led.brightness == 0.5
    
    # Test brightness bounds
    led.set_brightness(1.5)  # Should be clamped to 1.0
    assert led.brightness == 1.0
    
    led.set_brightness(-0.5)  # Should be clamped to 0.0
    assert led.brightness == 0.0
    
    print("✓ LED brightness control working correctly")


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Running Jukebox Tests")
    print("=" * 50)
    
    try:
        test_jukebox_initialization()
        test_playlist_operations()
        test_playback_controls()
        test_shuffle_and_repeat()
        test_volume_control()
        test_led_controller()
        test_led_brightness()
        
        print("\n" + "=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
