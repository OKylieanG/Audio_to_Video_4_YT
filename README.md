# Audio to Video Converter (Scaled Version)

A Python utility to combine audio files with static images OR video files to create YouTube-ready videos. Automatically scales to standard resolutions (1080p, 720p, or 480p).

## Features

- **Image Support**: Convert static images (JPG, PNG) with audio into video
- **Video Support**: Replace video file audio with a different audio track
- **Auto-scaling**: Scales large images/videos to standard resolutions
- **Memory efficient**: Handles large resolution files without memory errors

## Requirements

- Python 3.6+
- ffmpeg (must be installed separately)

### Installing ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**MacOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html and add to PATH

## Usage

### Using a Static Image

```bash
python audio_to_video_scaled.py cover.jpg song.mp3
```

This creates `song_video.mp4` using the image as static video background.

### Using a Video File

**Default behavior (video loops):**
```bash
python audio_to_video_scaled.py video.mov song.mp3
```

This strips the original audio from `video.mov` and replaces it with `song.mp3`. **By default, if the video is shorter than the audio, the video will loop** until the audio ends.

**Play video once, then show static image:**
```bash
python audio_to_video_scaled.py video.mov song.mp3 --fallback-image cover.jpg
```

This will:
1. Play the video once (with your audio replacing the original)
2. When the video ends, switch to showing `cover.jpg` as a static image
3. Continue showing the image until the audio finishes

**Example timeline:**
- Video: 30 seconds
- Audio: 3 minutes (180 seconds)
- Result: Video plays for 30s, then `cover.jpg` shows for the remaining 150s

### Disable Video Looping

```bash
python audio_to_video_scaled.py video.mov song.mp3 --no-loop
```

This will cut the output to whichever is shorter (video or audio), instead of looping.

**Note:** The `--fallback-image` option takes precedence over looping. If you specify both `--fallback-image` and `--no-loop`, the fallback image will be used.

### Specify Output Filename

```bash
python audio_to_video_scaled.py cover.jpg song.mp3 -o my_video.mp4
```

### Choose Resolution

```bash
python audio_to_video_scaled.py cover.jpg song.mp3 -r 720p
```

Resolution options:
- **480p**: 854x480 (smaller file size)
- **720p**: 1280x720 (HD)
- **1080p**: 1920x1080 (Full HD) - **default**

### Complete Examples

```bash
# Image with custom output and resolution
python audio_to_video_scaled.py "Album Cover.png" "My Song.mp3" -o "My Video.mp4" -r 1080p

# Video looping (default behavior)
python audio_to_video_scaled.py "footage.mov" "soundtrack.mp3" -o "final.mp4"

# Video with fallback image (video plays once, then image)
python audio_to_video_scaled.py "intro.mov" "full_song.mp3" --fallback-image "album_art.jpg" -o "music_video.mp4"

# Video at 720p resolution with fallback
python audio_to_video_scaled.py "video.mp4" "audio.mp3" --fallback-image "cover.jpg" -r 720p

# Video cut to shortest (no looping)
python audio_to_video_scaled.py "clip.mov" "long_audio.mp3" --no-loop -o "short.mp4"
```

## Command-Line Options

```
positional arguments:
  video_or_image        Path to image file (.jpg, .png) or video file (.mov, .mp4, etc.)
  audio                 Path to audio file (.mp3, etc.)

optional arguments:
  -h, --help            Show help message
  -o OUTPUT, --output OUTPUT
                        Output video filename (default: <audio_name>_video.mp4)
  -r {480p,720p,1080p}, --resolution {480p,720p,1080p}
                        Video resolution (default: 1080p)
  --no-loop             Do not loop video (cut to shortest input instead)
  --fallback-image FALLBACK_IMAGE
                        Image to show after video ends (if video is shorter than audio)
```

**Mode Selection Logic:**
- Video + no options = **loops** until audio ends
- Video + `--fallback-image` = plays once, then shows **fallback image**
- Video + `--no-loop` = cuts to **shortest** input
- Image = always matches audio length (static)

## How It Works

### For Images:
1. Loops the static image for the duration of the audio
2. Scales the image to fit the target resolution (maintaining aspect ratio)
3. Adds black bars (letterbox/pillarbox) if needed to reach exact dimensions
4. Encodes as H.264 video with AAC audio

### For Videos:
The script supports three modes when using video files:

**1. Loop Mode (default):**
- Video loops continuously to match audio length
- Example: 30s video + 3min audio = video loops 6 times

**2. Fallback Image Mode (--fallback-image):**
- Video plays once with your audio
- When video ends, switches to a static fallback image
- Image displays for the remaining audio duration
- Example: 30s video + 3min audio = 30s video, then 2.5min of static image

**3. No-Loop Mode (--no-loop):**
- Output ends when the shorter input ends
- No looping, no fallback image

**Technical details:**
1. Strips the original audio track from the video
2. Replaces it with the provided audio file
3. Scales video to target resolution (maintaining aspect ratio)
4. Adds black bars if needed to reach exact dimensions
5. Encodes as H.264 with AAC audio
6. For fallback mode: uses filter_complex to concatenate video and image segments

## Output Format

Videos are created with:
- **Video codec**: H.264 (libx264)
- **Audio codec**: AAC at 192kbps
- **Pixel format**: yuv420p (maximum compatibility)
- **Container**: MP4 with faststart flag (optimized for streaming)

## Supported Video Formats

Input video formats: `.mov`, `.mp4`, `.avi`, `.mkv`, `.wmv`, `.flv`, `.webm`, `.m4v`, `.mpg`, `.mpeg`

The script automatically detects whether the input is a video or image based on the file extension.

## Why This Version?

This "scaled" version is specifically designed to:
1. Handle very large images (e.g., 4032x3024 from phone cameras) without memory errors
2. Produce YouTube-optimized output resolutions
3. Reduce file sizes while maintaining good quality
4. Work reliably on systems with limited RAM
5. Support flexible video handling (loop, fallback image, or cut to shortest)

## Use Cases

**Static Image Mode:**
- Podcast episodes with cover art
- Simple lyric videos
- Audio visualizations with album artwork

**Video Loop Mode:**
- Short b-roll footage that loops throughout a song
- Animated backgrounds
- Performance clips that repeat

**Fallback Image Mode:**
- Music videos: intro clip → album art
- Tutorial videos: demonstration → contact info slide
- Concert footage: short clip → band logo for remainder
- Vlogs: opening sequence → static thumbnail

## Troubleshooting

**Video is the wrong aspect ratio**
- The script maintains original aspect ratio and adds black bars as needed
- This prevents distortion/stretching

**File size is too large**
- Use `-r 720p` or `-r 480p` for smaller files
- YouTube will re-encode anyway, so 720p is often sufficient

**Video is shorter than audio (or vice versa)**
- By default, videos loop automatically to match audio length
- Use `--no-loop` if you want the output to end when the video ends
- If you want different behavior, you can edit the video or audio separately first

**Video loops too many times / looks repetitive**
- Consider using a longer video clip
- Or use a static image instead for cleaner results
- Or trim your audio to match the video length before processing
