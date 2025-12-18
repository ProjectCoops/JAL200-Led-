# Quick Start Guide - Raspberry Pi Jukebox

## 1. Installation

```bash
# Clone the repository
git clone https://github.com/ProjectCoops/JAL200-Led-.git
cd JAL200-Led-

# Install dependencies
pip3 install -r requirements.txt

# Optional: Install GPIO support for LEDs (Raspberry Pi only)
pip3 install RPi.GPIO
```

## 2. Try the Demo

See all features in action without needing audio files:

```bash
python3 demo.py
```

## 3. Add Your Music

Create a music directory and add your audio files:

```bash
mkdir music
# Copy your MP3, WAV, OGG, FLAC, or M4A files to the music folder
```

## 4. Run the Jukebox

```bash
python3 jukebox.py
```

## 5. Basic Commands

Once running, try these commands:

- `load music` - Load all songs from the music directory
- `list` - Show all tracks
- `play 1` - Play the first track
- `next` - Skip to next song
- `pause` - Pause playback
- `resume` - Resume playback
- `shuffle` - Toggle shuffle mode
- `volume 75` - Set volume to 75%
- `quit` - Exit

## 6. Enable LED Control (Optional)

For visual feedback with LEDs:

1. Connect RGB LEDs to GPIO pins 17 (red), 27 (green), 22 (blue)
2. Edit `config.json` and set `"led_enabled": true`
3. Run with sudo: `sudo python3 jukebox.py`

LED colors indicate:
- **Green** = Playing
- **Yellow** = Paused
- **Red** = Stopped

## 7. Configuration

Edit `config.json` to customize:

```json
{
    "music_dir": "./music",
    "volume": 0.7,
    "led_enabled": false,
    "default_playlist": "./music"
}
```

## Troubleshooting

**No sound?**
- Check your speakers are connected
- Test with: `speaker-test -t wav`
- Adjust volume: `alsamixer`

**pygame not found?**
- Install it: `pip3 install pygame`

**LED control not working?**
- Run with sudo: `sudo python3 jukebox.py`
- Check GPIO connections
- Install RPi.GPIO: `pip3 install RPi.GPIO`

## More Help

See the full [README.md](README.md) for detailed documentation.
