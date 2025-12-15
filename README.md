# 🎬 AI Video Generator

A powerful Python tool for creating professional videos with background music, voice-overs, and stunning visual effects - **no API keys required!**

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 🎨 **Visual Effects**: Gradient, vignette, and blur effects
- 📹 **Camera Effects**: Zoom, pan, and static camera movements
- 🎵 **Background Music**: Add and loop background music with volume control
- 🎤 **Voice-Over Narration**: Text-to-speech for automated voice-overs
- 📝 **Text Overlays**: Add custom text to any scene
- 🎞️ **Smooth Transitions**: Fade in/out effects between scenes
- 💾 **HD Export**: 1920x1080 resolution output

## 📋 Requirements

### Required Dependencies
```bash
pip install moviepy pillow numpy
```

### Optional Dependencies
For voice-over narration:
```bash
pip install pyttsx3
```

### System Requirements
- **FFmpeg**: Required for video encoding
  - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
  - **Mac**: `brew install ffmpeg`
  - **Linux**: `sudo apt-get install ffmpeg`

## 🚀 Quick Start

### Basic Usage

```python
from main import AIVideoGenerator

# Initialize generator
generator = AIVideoGenerator()

# Define your scenes
scenes = [
    "A beautiful sunset over mountains",
    "A bustling city at night",
    "A peaceful forest with morning mist"
]

# Generate video
video_path = generator.generate_video(
    prompts=scenes,
    scene_duration=5.0,
    output_filename="my_video.mp4"
)

print(f"Video saved to: {video_path}")
```

### Advanced Usage with All Features

```python
from main import AIVideoGenerator

generator = AIVideoGenerator()

# Scene descriptions
prompts = [
    "Majestic mountain sunrise",
    "Futuristic city with neon lights",
    "Underwater coral reef"
]

# Text to display on screen
text_overlays = [
    "Chapter 1: The Beginning",
    "Chapter 2: The Future",
    "Chapter 3: The Depths"
]

# Voice-over narration
voice_overs = [
    "Our journey begins in the mountains",
    "We travel to a city of tomorrow",
    "And dive deep beneath the waves"
]

# Camera movements for each scene
camera_effects = ["zoom", "pan", "zoom"]

# Background visual effects
visual_effects = ["gradient", "vignette", "blur"]

# Generate complete video
video_path = generator.generate_video(
    prompts=prompts,
    scene_duration=7.0,
    text_overlays=text_overlays,
    camera_effects=camera_effects,
    visual_effects=visual_effects,
    background_music="background.mp3",  # Your music file
    voice_over_texts=voice_overs,
    music_volume=0.3,
    output_filename="complete_video.mp4"
)

# Clean up temporary files
generator.cleanup_temp_files()
```

## 🎮 Configuration Options

### Scene Duration
Control how long each scene displays:
```python
scene_duration=5.0  # 5 seconds per scene
```

### Camera Effects
Choose from three camera movements:
- `"zoom"` - Gradually zoom into the scene
- `"pan"` - Pan across the scene horizontally
- `"static"` - No camera movement

```python
camera_effects=["zoom", "pan", "static"]
```

### Visual Effects
Apply background effects:
- `"gradient"` - Color gradient overlay
- `"vignette"` - Darkened edges effect
- `"blur"` - Soft blur effect
- `"none"` - No effect

```python
visual_effects=["gradient", "vignette", "blur"]
```

### Background Music
Add music with volume control:
```python
background_music="path/to/music.mp3",
music_volume=0.3  # 0.0 (mute) to 1.0 (full volume)
```

### Text Overlays
Add text to scenes (supports multi-line with `\n`):
```python
text_overlays=[
    "Welcome to our story",
    "Line 1\nLine 2",  # Multi-line text
    "The End"
]
```

### Voice-Over Narration
Add automated voice narration:
```python
voice_over_texts=[
    "Welcome to this presentation",
    "Here we explore new ideas",
    "Thank you for watching"
]
```

## 📁 Project Structure

```
your-project/
│
├── main.py                 # Main video generator script
├── generated_videos/       # Output folder (auto-created)
│   ├── temp/              # Temporary files (auto-cleaned)
│   └── your_video.mp4     # Generated videos
│
└── assets/                # Optional: Your media files
    ├── music.mp3
    └── logo.png
```

## 🎯 Use Cases

- 🎓 **Educational Content**: Create tutorial videos
- 📱 **Social Media**: Generate content for Instagram, TikTok, YouTube
- 💼 **Marketing**: Product presentations and promos
- 📊 **Presentations**: Automated slide shows
- 🎨 **Creative Projects**: Storytelling and art videos
- 📰 **News Summaries**: Quick video news updates

## 🛠️ Troubleshooting

### "Import moviepy.editor could not be resolved"
This is a VS Code warning, not an error. The code will run fine. To fix:
1. Press `Ctrl+Shift+P`
2. Type "Reload Window"
3. Press Enter

### "FFmpeg not found"
Install FFmpeg on your system:
- Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Mac: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

### Voice-over not working
Install the text-to-speech library:
```bash
pip install pyttsx3
```

### Video export fails
Make sure you have enough disk space and write permissions in the output directory.

### Music file not found
Use absolute paths or place music files in the same directory as `main.py`:
```python
background_music="C:/Users/YourName/Music/song.mp3"
# or
background_music="./music.mp3"
```

## 🎨 Customization Tips

### Adjust Text Appearance
Edit the `_draw_text_with_outline()` method to change:
- Font size
- Font family
- Text color
- Outline thickness

### Change Image Colors
Modify the color generation in `generate_image_from_prompt()`:
```python
base_color = (255, 100, 100)  # Red-tinted backgrounds
```

### Adjust Zoom Speed
Change the zoom factor in `create_scene()`:
```python
zoom_factor = 1 + (t / duration) * 0.3  # 30% zoom instead of 20%
```

## 📝 Examples

### Example 1: Simple 3-Scene Video
```python
generator = AIVideoGenerator()

video = generator.generate_video(
    prompts=[
        "Morning coffee",
        "Afternoon work",
        "Evening relaxation"
    ],
    scene_duration=4.0,
    output_filename="my_day.mp4"
)
```

### Example 2: Video with Music
```python
generator = AIVideoGenerator()

video = generator.generate_video(
    prompts=["Scene 1", "Scene 2", "Scene 3"],
    background_music="happy_music.mp3",
    music_volume=0.5,
    output_filename="video_with_music.mp4"
)
```

### Example 3: Full-Featured Video
```python
generator = AIVideoGenerator()

video = generator.generate_video(
    prompts=["Opening", "Main Content", "Closing"],
    text_overlays=["Welcome", "Key Points", "Thank You"],
    voice_over_texts=["Hi everyone", "Let me explain", "Thanks for watching"],
    camera_effects=["zoom", "pan", "static"],
    visual_effects=["gradient", "vignette", "blur"],
    background_music="background.mp3",
    music_volume=0.3,
    scene_duration=6.0,
    output_filename="complete_video.mp4"
)

generator.cleanup_temp_files()
```

## 📄 License

- This project is open source and available under the MIT License.

## 🤝 Contributing

- Contributions, issues, and feature requests are welcome!

## 💡 Tips for Best Results
1. **Scene Duration**: 5-7 seconds works well for most content
2. **Music Volume**: Keep between 0.2-0.4 for background music
3. **Text Overlays**: Keep text short and readable (max 2-3 lines)
4. **Camera Effects**: Alternate between zoom and pan for variety
5. **Visual Effects**: Use gradient for most scenes, vignette for dramatic effect
6. **Voice-Overs**: Keep sentences short and clear

## 🌟 Credits

Created with ❤️ using:
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing
- [Pillow](https://python-pillow.org/) - Image processing
- [pyttsx3](https://pyttsx3.readthedocs.io/) - Text-to-speech

---

**Made with Python | Generate amazing videos in minutes! 🎥✨**
