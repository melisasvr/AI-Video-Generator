"""
AI Video Generator with Background Music, Voice Over, and Visual Effects
No APIs needed - Simple and powerful!
"""

import os
from pathlib import Path
from typing import List, Optional, Literal
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from moviepy.editor import (
    ImageClip, CompositeVideoClip, CompositeAudioClip,
    AudioFileClip, concatenate_videoclips
)
from moviepy.video.fx.all import fadein, fadeout
import random


class AIVideoGenerator:
    """Generate videos with music, voice overs, and visual effects"""
    
    def __init__(self, output_dir: str = "generated_videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = self.output_dir / "temp"
        self.temp_dir.mkdir(exist_ok=True)
        
    def generate_image_from_prompt(self, prompt: str, index: int, 
                                   text_overlay: Optional[str] = None,
                                   visual_effect: str = "none") -> str:
        """
        Generate an image with colored background, text, and visual effects
        """
        # Create base image with color based on prompt
        base_color = (
            hash(prompt) % 200 + 50,
            (hash(prompt) * 2) % 200 + 50,
            (hash(prompt) * 3) % 200 + 50
        )
        img = Image.new('RGB', (1920, 1080), color=base_color)
        
        # Apply visual effects to background
        if visual_effect == "blur":
            img = img.filter(ImageFilter.GaussianBlur(radius=15))
        elif visual_effect == "gradient":
            img = self._add_gradient(img, base_color)
        elif visual_effect == "vignette":
            img = self._add_vignette(img)
        
        draw = ImageDraw.Draw(img)
        
        # Load fonts
        try:
            title_font = ImageFont.truetype("arial.ttf", 70)
            overlay_font = ImageFont.truetype("arial.ttf", 55)
        except:
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
                overlay_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
            except:
                title_font = ImageFont.load_default()
                overlay_font = ImageFont.load_default()
        
        # Add scene number at top
        text = f"Scene {index + 1}"
        self._draw_text_with_outline(draw, text, (960, 350), title_font, 'white', 'black')
        
        # Add text overlay in the CENTER if provided
        if text_overlay:
            self._draw_text_with_outline(draw, text_overlay, (960, 540), overlay_font, 'white', 'black')
        
        img_path = self.temp_dir / f"scene_{index}.png"
        img.save(img_path)
        return str(img_path)
    
    def _add_gradient(self, img: Image.Image, base_color: tuple) -> Image.Image:
        """Add a gradient effect to the image"""
        gradient = Image.new('RGB', img.size)
        draw = ImageDraw.Draw(gradient)
        
        for y in range(img.size[1]):
            progress = y / img.size[1]
            color = tuple(int(c * (1 - progress * 0.5)) for c in base_color)
            draw.line([(0, y), (img.size[0], y)], fill=color)
        
        return Image.blend(img, gradient, 0.7)
    
    def _add_vignette(self, img: Image.Image) -> Image.Image:
        """Add a vignette (darkened edges) effect"""
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        
        for i in range(255):
            xy = (i, i, img.size[0]-i, img.size[1]-i)
            draw.rectangle(xy, fill=i)
        
        mask = mask.filter(ImageFilter.GaussianBlur(radius=100))
        
        overlay = Image.new('RGB', img.size, (0, 0, 0))
        return Image.composite(img, overlay, mask)
    
    def _draw_text_with_outline(self, draw, text, position, font, fill_color, outline_color, outline_width=4):
        """Draw text with outline for better visibility"""
        x, y = position
        
        # Get text size for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x = x - text_width // 2
        y = y - text_height // 2
        
        # Draw outline
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=fill_color)
    
    def create_scene(self, image_path: str, duration: float, 
                     effect: Literal["zoom", "pan", "static"] = "zoom") -> ImageClip:
        """Create a video scene with various camera effects"""
        clip = ImageClip(image_path).set_duration(duration)
        
        if effect == "zoom":
            def zoom_in(get_frame, t):
                frame = get_frame(t)
                zoom_factor = 1 + (t / duration) * 0.2  # 20% zoom
                h, w = frame.shape[:2]
                new_h, new_w = int(h / zoom_factor), int(w / zoom_factor)
                top = (h - new_h) // 2
                left = (w - new_w) // 2
                cropped = frame[top:top+new_h, left:left+new_w]
                return np.array(Image.fromarray(cropped).resize((w, h), Image.Resampling.LANCZOS))
            clip = clip.fl(zoom_in)
            
        elif effect == "pan":
            def pan_right(get_frame, t):
                frame = get_frame(t)
                h, w = frame.shape[:2]
                shift = int((t / duration) * w * 0.1)  # Pan 10% across
                if shift > 0:
                    frame = np.roll(frame, -shift, axis=1)
                return frame
            clip = clip.fl(pan_right)
        
        # Add fade transitions
        clip = fadein(clip, 0.5)
        clip = fadeout(clip, 0.5)
        
        return clip
    
    def text_to_speech(self, text: str, output_path: str) -> bool:
        """
        Generate voice over from text using text-to-speech
        Requires: pip install pyttsx3 (for offline TTS)
        
        Returns True if successful, False otherwise
        """
        try:
            import pyttsx3
            engine = pyttsx3.init()
            
            # Configure voice settings
            engine.setProperty('rate', 150)  # Speed of speech
            engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
            
            # Save to file
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            return True
        except ImportError:
            print("⚠️  pyttsx3 not installed. Run: pip install pyttsx3")
            return False
        except Exception as e:
            print(f"⚠️  Text-to-speech failed: {e}")
            return False
    
    def generate_video(self, 
                      prompts: List[str],
                      scene_duration: float = 7.0,
                      text_overlays: Optional[List[str]] = None,
                      camera_effects: Optional[List[str]] = None,
                      visual_effects: Optional[List[str]] = None,
                      background_music: Optional[str] = None,
                      voice_over_texts: Optional[List[str]] = None,
                      music_volume: float = 0.3,
                      output_filename: str = "output_video.mp4") -> str:
        """
        Generate a complete video with all features
        
        Args:
            prompts: List of text prompts for scene generation
            scene_duration: Duration of each scene in seconds
            text_overlays: Text to display on each scene
            camera_effects: List of effects per scene: "zoom", "pan", or "static"
            visual_effects: List of visual effects: "none", "gradient", "vignette", "blur"
            background_music: Path to background music file
            voice_over_texts: Text to convert to speech for each scene
            music_volume: Background music volume (0.0 to 1.0)
            output_filename: Output video filename
        
        Returns:
            Path to generated video
        """
        print("🎬 Starting video generation...")
        
        # Set default effects if not provided
        if camera_effects is None:
            camera_effects = ["zoom"] * len(prompts)
        if visual_effects is None:
            visual_effects = ["gradient"] * len(prompts)
        
        # Generate voice overs if requested
        voice_files = []
        if voice_over_texts:
            print("🎤 Generating voice overs...")
            for i, voice_text in enumerate(voice_over_texts):
                if voice_text:
                    voice_path = self.temp_dir / f"voice_{i}.mp3"
                    if self.text_to_speech(voice_text, str(voice_path)):
                        voice_files.append(str(voice_path))
                        print(f"  ✅ Voice over {i+1} generated")
                    else:
                        voice_files.append(None)
                else:
                    voice_files.append(None)
        
        # Generate images for each prompt
        print(f"📸 Generating {len(prompts)} scenes...")
        image_paths = []
        for i, prompt in enumerate(prompts):
            overlay = text_overlays[i] if text_overlays and i < len(text_overlays) else None
            effect = visual_effects[i] if i < len(visual_effects) else "none"
            print(f"  Scene {i+1}/{len(prompts)}: {prompt}")
            img_path = self.generate_image_from_prompt(prompt, i, overlay, effect)
            image_paths.append(img_path)
        
        # Create video clips
        print("🎞️  Creating video clips with effects...")
        clips = []
        for i, img_path in enumerate(image_paths):
            cam_effect = camera_effects[i] if i < len(camera_effects) else "zoom"
            clip = self.create_scene(img_path, scene_duration, cam_effect)
            
            # Add voice over audio to this clip if available
            if voice_files and i < len(voice_files) and voice_files[i]:
                try:
                    voice_audio = AudioFileClip(voice_files[i])
                    clip = clip.set_audio(voice_audio)
                except Exception as e:
                    print(f"  ⚠️  Could not add voice to scene {i+1}: {e}")
            
            clips.append(clip)
        
        # Concatenate clips
        print("✂️  Combining clips...")
        final_clip = concatenate_videoclips(clips, method="compose")
        
        # Add background music
        if background_music and os.path.exists(background_music):
            print("🎵 Adding background music...")
            try:
                music = AudioFileClip(background_music)
                
                # Loop music if it's shorter than video
                if music.duration < final_clip.duration:
                    music = music.audio_loop(duration=final_clip.duration)
                else:
                    music = music.subclip(0, final_clip.duration)
                
                # Adjust volume
                music = music.volumex(music_volume)
                
                # Mix with voice over if present
                if final_clip.audio:
                    final_audio = CompositeAudioClip([final_clip.audio, music])
                    final_clip = final_clip.set_audio(final_audio)
                else:
                    final_clip = final_clip.set_audio(music)
                    
            except Exception as e:
                print(f"⚠️  Could not add background music: {e}")
        
        # Export video
        output_path = self.output_dir / output_filename
        print(f"💾 Exporting video to {output_path}...")
        final_clip.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac'
        )
        
        print(f"✅ Video generated successfully: {output_path}")
        return str(output_path)
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        for file in self.temp_dir.glob("*"):
            file.unlink()
        print("🧹 Temporary files cleaned up")


# Example usage
if __name__ == "__main__":
    # Initialize generator
    generator = AIVideoGenerator()
    
    # Define your video content
    prompts = [
        "A serene mountain landscape at sunrise with golden light",
        "A bustling futuristic city with flying cars and neon lights",
        "An underwater coral reef teeming with colorful fish",
        "A cozy coffee shop with warm lighting and books on shelves",
        "A peaceful zen garden with cherry blossoms falling",
        "A dramatic storm over an ocean with lightning strikes"
    ]
    
    # Text overlays that appear on screen
    text_overlays = [
        "Our journey begins in the mountains,\nwhere peace meets adventure",
        "The future awaits with endless\npossibilities and new discoveries",
        "Deep beneath the waves,\nlife thrives in vibrant colors",
        "Finding comfort in simple moments,\nwhere stories come alive",
        "Nature's beauty reminds us to\nstay calm and centered",
        "Even in chaos, there is power\nand breathtaking beauty"
    ]
    
    # Voice over narration (optional - requires pyttsx3)
    voice_overs = [
        "Welcome to a journey through different worlds.",
        "Each scene tells a unique story.",
        "From the depths of the ocean to the heights of mountains.",
        "Finding peace in every moment.",
        "Embracing nature's tranquility.",
        "And discovering beauty in the storm."
    ]
    
    # Camera effects for each scene
    camera_effects = ["zoom", "pan", "zoom", "static", "zoom", "pan"]
    
    # Visual effects for backgrounds
    visual_effects = ["gradient", "vignette", "gradient", "blur", "gradient", "vignette"]
    
    # Generate video with all features
    video_path = generator.generate_video(
        prompts=prompts,
        scene_duration=7.0,
        text_overlays=text_overlays,
        camera_effects=camera_effects,
        visual_effects=visual_effects,
        background_music="music.mp3",  # Add your music file here
        voice_over_texts=voice_overs,  # Comment out if you don't want voice
        music_volume=0.3,  # 30% volume for background music
        output_filename="my_ai_video.mp4"
    )
    
    # Clean up
    generator.cleanup_temp_files()
    
    print(f"\n🎉 All done! Your video is ready at: {video_path}")
    print("\n📝 Features included:")
    print("  ✅ Visual effects (gradient, vignette, blur)")
    print("  ✅ Camera effects (zoom, pan, static)")
    print("  ✅ Background music support")
    print("  ✅ Voice over narration (requires: pip install pyttsx3)")