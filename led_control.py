#!/usr/bin/env python3
"""
LED Control Module for JAL200 LED Display
Provides simple LED control interface for the jukebox
"""

import time
from typing import Optional


class LEDController:
    """Control LEDs for visual feedback"""
    
    def __init__(self, enabled: bool = False):
        """Initialize LED controller"""
        self.enabled = enabled
        self.current_color = "off"
        self.brightness = 1.0
        
        # Try to import RPi.GPIO for Raspberry Pi LED control
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.gpio_available = True
            self._setup_gpio()
        except (ImportError, RuntimeError):
            self.GPIO = None
            self.gpio_available = False
            print("Note: RPi.GPIO not available. LED control will be simulated.")
    
    def _setup_gpio(self):
        """Setup GPIO pins for LED control"""
        if not self.gpio_available or not self.enabled:
            return
        
        # Setup GPIO pins (example configuration for RGB LED)
        # Adjust these pin numbers based on your actual hardware setup
        self.RED_PIN = 17
        self.GREEN_PIN = 27
        self.BLUE_PIN = 22
        
        try:
            self.GPIO.setmode(self.GPIO.BCM)
            self.GPIO.setwarnings(False)
            self.GPIO.setup(self.RED_PIN, self.GPIO.OUT)
            self.GPIO.setup(self.GREEN_PIN, self.GPIO.OUT)
            self.GPIO.setup(self.BLUE_PIN, self.GPIO.OUT)
            
            # Setup PWM for brightness control
            self.red_pwm = self.GPIO.PWM(self.RED_PIN, 100)
            self.green_pwm = self.GPIO.PWM(self.GREEN_PIN, 100)
            self.blue_pwm = self.GPIO.PWM(self.BLUE_PIN, 100)
            
            self.red_pwm.start(0)
            self.green_pwm.start(0)
            self.blue_pwm.start(0)
        except Exception as e:
            print(f"GPIO setup error: {e}")
            self.gpio_available = False
    
    def set_color(self, color: str, brightness: Optional[float] = None):
        """
        Set LED color
        Supported colors: red, green, blue, yellow, cyan, magenta, white, off
        """
        if not self.enabled:
            return
        
        if brightness is not None:
            self.brightness = max(0.0, min(1.0, brightness))
        
        self.current_color = color.lower()
        
        # Color definitions (RGB values 0-100 for PWM)
        colors = {
            "red": (100, 0, 0),
            "green": (0, 100, 0),
            "blue": (0, 0, 100),
            "yellow": (100, 100, 0),
            "cyan": (0, 100, 100),
            "magenta": (100, 0, 100),
            "white": (100, 100, 100),
            "off": (0, 0, 0),
        }
        
        if color.lower() not in colors:
            print(f"Unknown color: {color}")
            return
        
        r, g, b = colors[color.lower()]
        
        # Apply brightness
        r = int(r * self.brightness)
        g = int(g * self.brightness)
        b = int(b * self.brightness)
        
        if self.gpio_available:
            try:
                self.red_pwm.ChangeDutyCycle(r)
                self.green_pwm.ChangeDutyCycle(g)
                self.blue_pwm.ChangeDutyCycle(b)
            except Exception as e:
                print(f"LED control error: {e}")
        else:
            # Simulate LED control with console output
            if color.lower() != "off":
                print(f"[LED] Color: {color} (Brightness: {int(self.brightness * 100)}%)")
    
    def pulse(self, color: str, duration: float = 1.0, cycles: int = 3):
        """Pulse LED color for visual effect"""
        if not self.enabled:
            return
        
        original_brightness = self.brightness
        
        for _ in range(cycles):
            # Fade in
            for i in range(0, 101, 10):
                self.set_color(color, i / 100.0)
                time.sleep(duration / 20)
            
            # Fade out
            for i in range(100, -1, -10):
                self.set_color(color, i / 100.0)
                time.sleep(duration / 20)
        
        # Restore original brightness
        self.brightness = original_brightness
        self.set_color(color, original_brightness)
    
    def blink(self, color: str, interval: float = 0.5, count: int = 5):
        """Blink LED on and off"""
        if not self.enabled:
            return
        
        for _ in range(count):
            self.set_color(color)
            time.sleep(interval)
            self.set_color("off")
            time.sleep(interval)
    
    def set_brightness(self, brightness: float):
        """Set LED brightness (0.0 to 1.0)"""
        self.brightness = max(0.0, min(1.0, brightness))
        # Re-apply current color with new brightness
        if self.current_color != "off":
            self.set_color(self.current_color)
    
    def cleanup(self):
        """Cleanup GPIO resources"""
        if self.gpio_available and self.enabled:
            try:
                self.red_pwm.stop()
                self.green_pwm.stop()
                self.blue_pwm.stop()
                self.GPIO.cleanup()
            except Exception as e:
                print(f"GPIO cleanup error: {e}")


# Singleton instance
_led_controller: Optional[LEDController] = None


def get_led_controller(enabled: bool = False) -> LEDController:
    """Get or create LED controller singleton"""
    global _led_controller
    if _led_controller is None:
        _led_controller = LEDController(enabled)
    return _led_controller


if __name__ == "__main__":
    # Test LED controller
    print("Testing LED Controller...")
    led = LEDController(enabled=True)
    
    colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "white"]
    
    print("\nTesting colors...")
    for color in colors:
        led.set_color(color)
        time.sleep(0.5)
    
    led.set_color("off")
    
    print("\nTesting pulse effect...")
    led.pulse("green", duration=0.5, cycles=2)
    
    print("\nTesting blink effect...")
    led.blink("red", interval=0.3, count=3)
    
    led.set_color("off")
    led.cleanup()
    
    print("\nLED Controller test complete!")
