# Sprite Animator

A Python tool for converting sprite sheets into animations. Supports both animated GIF output and HTML/CSS animations.

## Features

- 🎬 Convert horizontal sprite sheets to animated GIFs
- 🌐 Generate HTML/CSS sprite animations
- ⚡ Fast, optimized output
- 🎨 Pixel-perfect rendering with configurable frame timing
- 🔧 Both CLI and Python API

## Installation

### For Users

```bash
pip install -e .
```

### For Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

## Quick Start

### Command Line

```bash
# Basic usage (creates animated GIF with 6 frames, 100ms each)
sprite-animator walk_sprite.png

# Specify output filename and frame count
sprite-animator walk_sprite.png -o walk.gif -n 8

# Adjust animation speed (50ms = faster)
sprite-animator walk_sprite.png -d 50

# Create HTML/CSS animation
sprite-animator walk_sprite.png --format html -o walk.html

# Create both formats
sprite-animator walk_sprite.png --format both

# Get sprite sheet info
sprite-animator walk_sprite.png --info
```

### Python API

```python
from sprite_animator import SpriteAnimator

# Load sprite sheet
animator = SpriteAnimator("walk_sprite.png")

# Create animated GIF
animator.create_gif(
    "output.gif",
    num_frames=6,
    duration=100,  # milliseconds per frame
    loop=0  # 0 = infinite loop
)

# Create HTML/CSS animation
animator.create_sprite_sheet_html(
    "output.html",
    num_frames=6,
    frame_duration=100,
    scale=2  # 2x display size
)

# Get sprite sheet info
info = animator.get_info()
print(f"Dimensions: {info['width']}x{info['height']}")
```

## Requirements

- Python 3.8+
- Pillow (PIL) 10.0.0+

## Project Structure

```
sprite-animator/
├── src/
│   └── sprite_animator/
│       ├── __init__.py      # Package initialization
│       ├── animator.py      # Core SpriteAnimator class
│       └── cli.py           # Command-line interface
├── pyproject.toml           # Project configuration
├── README.md                # This file
└── .gitignore              # Git ignore rules
```

## CLI Options

```
usage: sprite-animator [-h] [-o OUTPUT] [-n NUM_FRAMES] [-d DURATION]
                       [--format {gif,html,both}] [--no-loop] [--no-optimize]
                       [--scale SCALE] [--info] [--version]
                       sprite_sheet

Convert sprite sheets into animations (GIF, HTML/CSS)

positional arguments:
  sprite_sheet          Path to the sprite sheet image

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output filename (default: animation.gif or animation.html)
  -n NUM_FRAMES, --num-frames NUM_FRAMES
                        Number of frames in the sprite sheet (default: 6)
  -d DURATION, --duration DURATION
                        Duration of each frame in milliseconds (default: 100)
  --format {gif,html,both}
                        Output format (default: gif)
  --no-loop             Don't loop the GIF animation (play once)
  --no-optimize         Don't optimize the GIF file size
  --scale SCALE         Display scale for HTML output (default: 2)
  --info                Show sprite sheet info and exit
  --version             show program's version number and exit
```

## Development

### Code Quality Tools

The project uses modern Python tooling:

- **black**: Code formatting (100 char line length)
- **ruff**: Fast linting (replaces flake8, isort)
- **mypy**: Static type checking
- **pytest**: Testing framework

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type check
mypy src/

# Run tests (when added)
pytest
```

### Adding Tests

Tests should be placed in a `tests/` directory:

```bash
mkdir tests
# Add test_*.py files
pytest
```

## How It Works

### Sprite Sheet Format

The tool expects a **horizontal sprite sheet** where each frame is placed side-by-side:

```
[Frame 1][Frame 2][Frame 3][Frame 4][Frame 5][Frame 6]
```

The sprite sheet width should be evenly divisible by the number of frames for best results.

### GIF Creation

1. Loads the sprite sheet image
2. Calculates frame width (total_width / num_frames)
3. Extracts each frame by cropping
4. Combines frames into an animated GIF with specified timing
5. Optimizes the output (optional)

### HTML/CSS Animation

1. References the original sprite sheet image
2. Uses CSS `background-position` animation
3. `steps()` timing function for pixel-perfect frame changes
4. Hardware-accelerated, smooth playback

## Troubleshooting

### "Package not found" when installing

Make sure you're in the project directory and using Python 3.8+:

```bash
python --version  # Should be 3.8 or higher
pip install -e .
```

### Frames look misaligned

The sprite sheet width must be evenly divisible by the number of frames. Check your sprite sheet dimensions:

```bash
sprite-animator your_sprite.png --info
```

### HTML animation not showing sprite

The HTML file references the sprite sheet by filename. Make sure both files are in the same directory.

## Contributing

This is a personal project, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Author

Nathan Norman (nathannorman@gmail.com)
