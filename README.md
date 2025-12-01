# C & J Simulator

A fun browser-based game featuring Jude bouncing on a trampoline! Works on desktop and mobile.

## Play the Game

**Live Demo:** [Play Now](https://nathannorman.github.io/cj-simulator/)

## How to Play

### Desktop (Keyboard)
- **Arrow Keys**: Move left/right
- **Up Arrow**: Jump
- **Shift + Arrows**: Move faster

### Mobile (Touch)
- **Left/Right Buttons**: Move
- **Jump Button**: Jump
- Rotate device to landscape mode for best experience

### Goal
Bounce on the trampoline 7 times in a row to win! Each bounce makes you go higher.

## Features

- Parallax scrolling backgrounds (mountains, hills, ground)
- Walk and jump sprite animations
- Physics-based trampoline with increasing bounce height
- Screen shake and visual effects on big bounces
- Win animation with character landing on mountain peak
- Fully responsive - works on desktop and mobile
- Touch controls for mobile play

## Deploy to GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings > Pages**
3. Under "Source", select **Deploy from a branch**
4. Select **main** branch and **/ (root)** folder
5. Click **Save**
6. Your game will be live at `https://YOUR-USERNAME.github.io/REPO-NAME/`

## Files

| File | Description |
|------|-------------|
| `index.html` | Main game (mobile + desktop) |
| `jude-demo.html` | Development version |
| `sprite-editor.html` | Tool for editing sprite frames |
| `jude-spritesheet.png` | Walk animation sprite sheet |
| `jude-jump-transparent.png` | Jump animation sprite sheet |

## Development

This is a single HTML file game with no build process. Just edit and refresh!

### Tools Included

- **Sprite Editor** (`sprite-editor.html`): Visual tool for defining animation frames on sprite sheets
- **GIF Creator** (`create_gif_from_json.py`): Python script to create GIFs from frame data

## Credits

- Game and animations by Nathan Norman
- Character art: Jude

## License

MIT License
