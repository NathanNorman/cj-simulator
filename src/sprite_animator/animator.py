"""
Core sprite animation functionality.
"""

from pathlib import Path
from typing import List, Optional

from PIL import Image


class SpriteAnimator:
    """Handles conversion of sprite sheets to animated formats."""

    def __init__(self, sprite_sheet_path: str | Path) -> None:
        """
        Initialize the animator with a sprite sheet.

        Args:
            sprite_sheet_path: Path to the sprite sheet image

        Raises:
            FileNotFoundError: If sprite sheet doesn't exist
            ValueError: If sprite sheet cannot be opened
        """
        self.sprite_sheet_path = Path(sprite_sheet_path)

        if not self.sprite_sheet_path.exists():
            raise FileNotFoundError(f"Sprite sheet not found: {self.sprite_sheet_path}")

        try:
            self.sprite_sheet = Image.open(self.sprite_sheet_path)
            self.width, self.height = self.sprite_sheet.size
        except Exception as e:
            raise ValueError(f"Failed to open sprite sheet: {e}") from e

    def extract_frames(self, num_frames: int) -> List[Image.Image]:
        """
        Extract individual frames from the sprite sheet.

        Args:
            num_frames: Number of frames in the horizontal sprite sheet

        Returns:
            List of PIL Image objects, one per frame

        Raises:
            ValueError: If num_frames is invalid
        """
        if num_frames <= 0:
            raise ValueError("Number of frames must be positive")

        if self.width % num_frames != 0:
            print(
                f"Warning: Width {self.width} not evenly divisible by {num_frames} frames. "
                f"Frames may be misaligned."
            )

        frame_width = self.width // num_frames
        frames = []

        for i in range(num_frames):
            left = i * frame_width
            box = (left, 0, left + frame_width, self.height)
            frame = self.sprite_sheet.crop(box)
            frames.append(frame)

        return frames

    def create_gif(
        self,
        output_path: str | Path,
        num_frames: int = 6,
        duration: int = 100,
        loop: int = 0,
        optimize: bool = True,
    ) -> Path:
        """
        Create an animated GIF from the sprite sheet.

        Args:
            output_path: Path for the output GIF file
            num_frames: Number of frames in the sprite sheet (default: 6)
            duration: Duration of each frame in milliseconds (default: 100)
            loop: Number of times to loop (0 = infinite, default: 0)
            optimize: Whether to optimize the GIF (default: True)

        Returns:
            Path to the created GIF file

        Raises:
            ValueError: If parameters are invalid
        """
        output_path = Path(output_path)

        if duration <= 0:
            raise ValueError("Duration must be positive")

        # Extract frames
        frames = self.extract_frames(num_frames)

        # Save as animated GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=loop,
            optimize=optimize,
        )

        return output_path

    def create_sprite_sheet_html(
        self,
        output_path: str | Path,
        num_frames: int = 6,
        frame_duration: int = 100,
        scale: int = 2,
    ) -> Path:
        """
        Create an HTML file with CSS sprite animation.

        Args:
            output_path: Path for the output HTML file
            num_frames: Number of frames in the sprite sheet (default: 6)
            frame_duration: Duration of each frame in milliseconds (default: 100)
            scale: Scale factor for display (default: 2x)

        Returns:
            Path to the created HTML file
        """
        output_path = Path(output_path)
        frame_width = self.width // num_frames
        total_duration_ms = frame_duration * num_frames

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sprite Animation</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #2c3e50;
            font-family: system-ui, -apple-system, sans-serif;
        }}

        .container {{
            text-align: center;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .sprite {{
            width: {frame_width}px;
            height: {self.height}px;
            background-image: url('{self.sprite_sheet_path.name}');
            background-repeat: no-repeat;
            animation: walk {total_duration_ms}ms steps({num_frames}) infinite;
            image-rendering: pixelated;
            transform: scale({scale});
            transform-origin: center;
            margin: 20px auto;
        }}

        @keyframes walk {{
            0% {{
                background-position: 0 0;
            }}
            100% {{
                background-position: -{self.width}px 0;
            }}
        }}

        h1 {{
            color: #2c3e50;
            margin: 0 0 20px 0;
        }}

        .info {{
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 20px;
        }}

        .controls {{
            margin-top: 20px;
        }}

        button {{
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin: 0 5px;
        }}

        button:hover {{
            background: #2980b9;
        }}

        button:active {{
            transform: translateY(1px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Sprite Animation</h1>
        <div class="sprite" id="sprite"></div>
        <div class="controls">
            <button onclick="toggleAnimation()">Pause/Play</button>
            <button onclick="resetAnimation()">Reset</button>
        </div>
        <div class="info">
            {num_frames} frames × {frame_duration}ms = {total_duration_ms}ms loop
        </div>
    </div>

    <script>
        const sprite = document.getElementById('sprite');
        let isPaused = false;

        function toggleAnimation() {{
            if (isPaused) {{
                sprite.style.animationPlayState = 'running';
            }} else {{
                sprite.style.animationPlayState = 'paused';
            }}
            isPaused = !isPaused;
        }}

        function resetAnimation() {{
            sprite.style.animation = 'none';
            setTimeout(() => {{
                sprite.style.animation = 'walk {total_duration_ms}ms steps({num_frames}) infinite';
                isPaused = false;
            }}, 10);
        }}
    </script>
</body>
</html>"""

        output_path.write_text(html_content)
        return output_path

    def get_info(self) -> dict:
        """
        Get information about the sprite sheet.

        Returns:
            Dictionary with sprite sheet dimensions and properties
        """
        return {
            "path": str(self.sprite_sheet_path),
            "width": self.width,
            "height": self.height,
            "format": self.sprite_sheet.format,
            "mode": self.sprite_sheet.mode,
        }
