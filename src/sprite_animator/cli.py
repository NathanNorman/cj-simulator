"""
Command-line interface for sprite animator.
"""

import argparse
import sys
from pathlib import Path

from sprite_animator.animator import SpriteAnimator


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog="sprite-animator",
        description="Convert sprite sheets into animations (GIF, HTML/CSS)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create animated GIF with defaults (6 frames, 100ms each)
  sprite-animator walk_sprite.png

  # Specify output filename and frame count
  sprite-animator walk_sprite.png -o walk.gif -n 8

  # Adjust animation speed (faster = lower duration)
  sprite-animator walk_sprite.png -d 50

  # Create both GIF and HTML versions
  sprite-animator walk_sprite.png --format both

  # Create only HTML with CSS animation
  sprite-animator walk_sprite.png --format html -o walk.html

  # Get sprite sheet info without creating animation
  sprite-animator walk_sprite.png --info
        """,
    )

    parser.add_argument("sprite_sheet", type=str, help="Path to the sprite sheet image")

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output filename (default: animation.gif or animation.html)",
    )

    parser.add_argument(
        "-n",
        "--num-frames",
        type=int,
        default=6,
        help="Number of frames in the sprite sheet (default: 6)",
    )

    parser.add_argument(
        "-d",
        "--duration",
        type=int,
        default=100,
        help="Duration of each frame in milliseconds (default: 100)",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["gif", "html", "both"],
        default="gif",
        help="Output format (default: gif)",
    )

    parser.add_argument(
        "--no-loop", action="store_true", help="Don't loop the GIF animation (play once)"
    )

    parser.add_argument(
        "--no-optimize", action="store_true", help="Don't optimize the GIF file size"
    )

    parser.add_argument(
        "--scale", type=int, default=2, help="Display scale for HTML output (default: 2)"
    )

    parser.add_argument("--info", action="store_true", help="Show sprite sheet info and exit")

    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    return parser


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        # Initialize animator
        animator = SpriteAnimator(args.sprite_sheet)

        # Show info and exit if requested
        if args.info:
            info = animator.get_info()
            print("Sprite Sheet Information:")
            print(f"  Path: {info['path']}")
            print(f"  Dimensions: {info['width']}x{info['height']}")
            print(f"  Format: {info['format']}")
            print(f"  Mode: {info['mode']}")
            print(f"  Frame width (for {args.num_frames} frames): {info['width'] // args.num_frames}")
            return 0

        # Determine output paths
        sprite_path = Path(args.sprite_sheet)
        base_name = sprite_path.stem

        if args.output:
            output_path = Path(args.output)
        else:
            if args.format == "html":
                output_path = Path(f"{base_name}_animation.html")
            else:
                output_path = Path(f"{base_name}_animation.gif")

        # Create animations based on format
        created_files = []

        if args.format in ("gif", "both"):
            gif_path = output_path if args.format == "gif" else output_path.with_suffix(".gif")
            print(f"Creating animated GIF...")
            print(f"  Frames: {args.num_frames}")
            print(f"  Duration: {args.duration}ms per frame")
            print(f"  Total loop time: {args.num_frames * args.duration}ms")

            animator.create_gif(
                gif_path,
                num_frames=args.num_frames,
                duration=args.duration,
                loop=1 if args.no_loop else 0,
                optimize=not args.no_optimize,
            )
            created_files.append(gif_path)
            print(f"✓ Created: {gif_path}")

        if args.format in ("html", "both"):
            html_path = output_path if args.format == "html" else output_path.with_suffix(".html")
            print(f"\nCreating HTML/CSS animation...")

            animator.create_sprite_sheet_html(
                html_path,
                num_frames=args.num_frames,
                frame_duration=args.duration,
                scale=args.scale,
            )
            created_files.append(html_path)
            print(f"✓ Created: {html_path}")
            print(f"  Note: Ensure '{sprite_path.name}' is in the same directory as the HTML file")

        # Summary
        print(f"\n✨ Successfully created {len(created_files)} animation(s)")
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nAborted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
