#!/usr/bin/env python3
"""
Create an animated GIF from a sprite sheet using frame data JSON.
"""

import json
import sys
import math
from pathlib import Path
from PIL import Image


def color_matches(pixel, bg_color, tolerance):
    """Check if a pixel color matches the background within tolerance."""
    dist = math.sqrt(
        (pixel[0] - bg_color[0])**2 +
        (pixel[1] - bg_color[1])**2 +
        (pixel[2] - bg_color[2])**2
    )
    max_dist = tolerance * 4.41
    return dist <= max_dist


def remove_background(image, bg_color=(255, 255, 255), tolerance=30):
    """Remove background using flood-fill from edges only.

    This preserves interior regions of the same color (like a white shirt)
    while removing the connected background from the edges.
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    width, height = image.size
    pixels = image.load()

    # Track which pixels to make transparent
    to_remove = set()
    visited = set()

    # Start flood fill from all edge pixels
    edge_pixels = []
    for x in range(width):
        edge_pixels.append((x, 0))           # Top edge
        edge_pixels.append((x, height - 1))  # Bottom edge
    for y in range(height):
        edge_pixels.append((0, y))           # Left edge
        edge_pixels.append((width - 1, y))   # Right edge

    # Flood fill from edges
    stack = []
    for pos in edge_pixels:
        if pos not in visited:
            x, y = pos
            pixel = pixels[x, y]
            if color_matches(pixel, bg_color, tolerance):
                stack.append(pos)

    while stack:
        x, y = stack.pop()

        if (x, y) in visited:
            continue
        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        visited.add((x, y))
        pixel = pixels[x, y]

        if color_matches(pixel, bg_color, tolerance):
            to_remove.add((x, y))
            # Add neighbors
            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))

    # Make the background pixels transparent
    for x, y in to_remove:
        r, g, b, a = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)

    return image


def create_gif(sprite_path: str, json_path: str, output_path: str = None,
               remove_bg: bool = False, bg_color=(255, 255, 255), tolerance=30):
    """Create animated GIF from sprite sheet and frame JSON."""

    # Load frame data
    with open(json_path) as f:
        data = json.load(f)

    frames_data = data['frames']
    speed = data.get('speed', 100)

    # Load sprite sheet
    sprite = Image.open(sprite_path)

    # Extract frames
    frames = []
    for fd in frames_data:
        box = (fd['x'], fd['y'], fd['x'] + fd['width'], fd['y'] + fd['height'])
        frame = sprite.crop(box)
        # Convert to RGBA for consistency
        if frame.mode != 'RGBA':
            frame = frame.convert('RGBA')

        # Remove background if requested
        if remove_bg:
            frame = remove_background(frame, bg_color, tolerance)

        frames.append(frame)

    if not frames:
        print("No frames to export!")
        return

    # Determine output path
    if not output_path:
        output_path = Path(sprite_path).stem + '_animation.gif'

    # Determine format from extension
    output_ext = Path(output_path).suffix.lower()

    if output_ext == '.png':
        # Save as APNG (animated PNG) - supports true alpha transparency
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=speed,
            loop=0
        )
    else:
        # Save as GIF - convert transparency to palette-based
        # GIF only supports 1-bit transparency
        gif_frames = []
        for frame in frames:
            # Create a new image with a magenta background (will become transparent)
            bg = Image.new('RGBA', frame.size, (255, 0, 255, 255))
            bg.paste(frame, mask=frame.split()[3])  # Paste using alpha as mask
            # Convert to palette mode with transparency
            gif_frame = bg.convert('P', palette=Image.ADAPTIVE, colors=255)
            # Set magenta as transparent
            gif_frame.info['transparency'] = gif_frame.getpixel((0, 0))
            gif_frames.append(gif_frame)

        gif_frames[0].save(
            output_path,
            save_all=True,
            append_images=gif_frames[1:],
            duration=speed,
            loop=0,
            disposal=2,
            transparency=gif_frames[0].info.get('transparency', 0)
        )

    print(f"✓ Created: {output_path}")
    print(f"  Frames: {len(frames)}")
    print(f"  Duration: {speed}ms per frame")
    print(f"  Frame size: {frames[0].width}x{frames[0].height}")
    if remove_bg:
        print(f"  Background removed: RGB{bg_color} (tolerance: {tolerance})")


def create_transparent_spritesheet(sprite_path: str, output_path: str,
                                    bg_color=(255, 255, 255), tolerance=30):
    """Create a copy of the sprite sheet with background removed."""
    sprite = Image.open(sprite_path)
    if sprite.mode != 'RGBA':
        sprite = sprite.convert('RGBA')

    result = remove_background(sprite, bg_color, tolerance)
    result.save(output_path)
    print(f"✓ Created transparent sprite sheet: {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Create animated GIF from sprite sheet')
    parser.add_argument('sprite', help='Path to sprite sheet image')
    parser.add_argument('json', nargs='?', help='Path to frame data JSON (not needed for --spritesheet)')
    parser.add_argument('-o', '--output', help='Output path')
    parser.add_argument('--remove-bg', action='store_true', help='Remove background color')
    parser.add_argument('--bg-color', default='255,255,255', help='Background color as R,G,B (default: 255,255,255)')
    parser.add_argument('--tolerance', type=int, default=30, help='Color tolerance 0-100 (default: 30)')
    parser.add_argument('--spritesheet', action='store_true', help='Output transparent sprite sheet instead of animation')

    args = parser.parse_args()

    bg_color = tuple(int(x) for x in args.bg_color.split(','))

    if args.spritesheet:
        output = args.output or args.sprite.replace('.png', '-transparent.png')
        create_transparent_spritesheet(args.sprite, output, bg_color, args.tolerance)
    else:
        if not args.json:
            print("Error: JSON file required for animation output")
            sys.exit(1)
        create_gif(
            args.sprite,
            args.json,
            args.output,
            remove_bg=args.remove_bg,
            bg_color=bg_color,
            tolerance=args.tolerance
        )
