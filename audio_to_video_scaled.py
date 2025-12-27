#!/usr/bin/env python3
"""
Audio to Video - Alternative version with forced dimensions
Scales image to standard video resolution (1920x1080)
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def create_video_scaled(image_path, audio_path, output_path=None, resolution='1080p'):
    """
    Create video with forced scaling to standard resolution.
    """
    # Normalize paths
    image_path = os.path.abspath(image_path)
    audio_path = os.path.abspath(audio_path)
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    if output_path is None:
        audio_name = Path(audio_path).stem
        output_path = f"{audio_name}_video.mp4"
    
    output_path = os.path.abspath(output_path)
    
    # Resolution presets
    resolutions = {
        '720p': '1280:720',
        '1080p': '1920:1080',
        '480p': '854:480'
    }
    
    scale = resolutions.get(resolution, '1920:1080')
    
    # Command with explicit scaling
    command = [
        'ffmpeg',
        '-loop', '1',
        '-i', image_path,
        '-i', audio_path,
        '-vf', f'scale={scale}:force_original_aspect_ratio=decrease,pad={scale}:(ow-iw)/2:(oh-ih)/2',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-movflags', '+faststart',
        '-y',
        output_path
    ]
    
    print(f"Creating video: {output_path}")
    print(f"Image: {image_path}")
    print(f"Audio: {audio_path}")
    print(f"Resolution: {resolution} ({scale})")
    print("\nProcessing...")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"\n✓ Video created successfully: {output_path}")
        
        if os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"  File size: {size_mb:.2f} MB")
        
        return output_path
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error creating video", file=sys.stderr)
        print(f"\nffmpeg error output:", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(f"\nCommand:", file=sys.stderr)
        print(' '.join(command), file=sys.stderr)
        raise


def main():
    parser = argparse.ArgumentParser(
        description='Create video with scaled image',
    )
    
    parser.add_argument('image', help='Path to image file')
    parser.add_argument('audio', help='Path to audio file')
    parser.add_argument('-o', '--output', help='Output video filename')
    parser.add_argument('-r', '--resolution',
                       choices=['480p', '720p', '1080p'],
                       default='1080p',
                       help='Video resolution (default: 1080p)')
    
    args = parser.parse_args()
    
    # Check for ffmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, 
                      check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ffmpeg is not installed or not in PATH", file=sys.stderr)
        sys.exit(1)
    
    try:
        create_video_scaled(args.image, args.audio, args.output, args.resolution)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()