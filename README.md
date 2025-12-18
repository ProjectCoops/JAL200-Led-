# JAL200-Led- Raspberry Pi Jukebox

A feature-rich music jukebox software for Raspberry Pi with JAL200 LED display support.

## Features

- 🎵 Play music files (MP3, WAV, OGG, FLAC, M4A)
- 📝 Playlist management
- 🎛️ Playback controls (play, pause, stop, next, previous)
- 🔀 Shuffle and repeat modes
- 🔊 Volume control
- 💡 LED visual feedback for playback status
- 🎨 Support for JAL200 LED displays
- 💻 Interactive command-line interface

## Hardware Requirements

- Raspberry Pi (any model with audio output)
- Optional: JAL200 LED display or RGB LEDs
- Speakers or audio output device

## Software Requirements

- Python 3.6 or higher
- pygame library for audio playback

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ProjectCoops/JAL200-Led-.git
cd JAL200-Led-
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. (Optional) For LED control on Raspberry Pi:
```bash
pip3 install RPi.GPIO
```

## Configuration

Edit `config.json` to customize settings:

```json
{
    "music_dir": "./music",
    "volume": 0.7,
    "led_enabled": false,
    "default_playlist": "./music"
}
```

### Configuration Options

- **music_dir**: Default directory for music files
- **volume**: Default volume level (0.0 to 1.0)
- **led_enabled**: Enable/disable LED control
- **default_playlist**: Path to default playlist or music directory

## Usage

### Basic Usage

Run the jukebox:
```bash
python3 jukebox.py
```

### Load a Playlist

```bash
python3 jukebox.py --load /path/to/music/folder
```

Or load a playlist file:
```bash
python3 jukebox.py --load playlist.txt
```

### Interactive Commands

Once running, use these commands:

- `play [n]` - Play track n (or current track)
- `pause` - Pause playback
- `resume` - Resume playback
- `stop` - Stop playback
- `next` - Play next track
- `prev` - Play previous track
- `shuffle` - Toggle shuffle mode
- `repeat` - Toggle repeat mode
- `volume n` - Set volume (0-100)
- `list` - Show current playlist
- `load path` - Load playlist from path
- `quit` - Exit jukebox

### Example Session

```
jukebox> load ./music
Loaded 10 tracks

jukebox> list
=== Playlist (10 tracks) ===
  1. song1.mp3
  2. song2.mp3
  ...

jukebox> play 1
Playing: song1.mp3

jukebox> shuffle
Shuffle: ON

jukebox> next
Playing: song5.mp3

jukebox> volume 80
Volume: 80%
```

## Playlist Format

Create a text file with one music file path per line:

```
/path/to/song1.mp3
/path/to/song2.mp3
./music/song3.mp3
```

Or simply point to a directory containing music files, and all supported audio files will be automatically loaded.

## LED Control

### Playback Status Indicators

When LED control is enabled:
- **Green**: Playing
- **Yellow**: Paused
- **Red**: Stopped

### LED Setup

For Raspberry Pi with RGB LEDs, connect:
- Red LED to GPIO 17
- Green LED to GPIO 27
- Blue LED to GPIO 22

Adjust pin numbers in `led_control.py` if using different GPIO pins.

### Enable LED Control

1. Set `led_enabled` to `true` in `config.json`
2. Run with appropriate permissions:
```bash
sudo python3 jukebox.py
```

## LED Module

The `led_control.py` module can be used independently:

```python
from led_control import get_led_controller

led = get_led_controller(enabled=True)
led.set_color("green")
led.pulse("blue", duration=1.0, cycles=3)
led.blink("red", interval=0.5, count=5)
led.cleanup()
```

## Directory Structure

```
JAL200-Led-/
├── jukebox.py          # Main jukebox application
├── led_control.py      # LED control module
├── config.json         # Configuration file
├── requirements.txt    # Python dependencies
├── playlist.txt        # Example playlist file
├── README.md           # Documentation
└── music/              # Music directory (create this)
```

## Troubleshooting

### No audio output

1. Check audio device configuration:
```bash
aplay -l
```

2. Test audio output:
```bash
speaker-test -t wav
```

3. Adjust volume:
```bash
alsamixer
```

### pygame not found

Install pygame:
```bash
pip3 install pygame
```

### LED control not working

1. Ensure running with sudo (required for GPIO access)
2. Check GPIO pin connections
3. Verify `led_enabled` is set to `true` in config.json
4. Install RPi.GPIO: `pip3 install RPi.GPIO`

### Permission errors

Run with sudo for GPIO access:
```bash
sudo python3 jukebox.py
```

## Development

### Running Tests

Test LED controller:
```bash
python3 led_control.py
```

### Adding Features

The jukebox is designed to be modular:
- Extend `Jukebox` class for new playback features
- Modify `LEDController` for custom LED patterns
- Add new commands in the main loop

## License

This project is open source. See repository for license details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Credits

Developed for the JAL200-Led- project to create an interactive music experience with visual feedback.
