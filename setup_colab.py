#!/usr/bin/env python3
"""
Setup script untuk Google Colab - Multimodal Emotion Recognition
Audio Feature Extraction Pipeline

Jalankan script ini di Google Colab untuk setup otomatis
"""

def setup_colab_environment():
    """Setup environment untuk Google Colab"""
    
    print("=== Setting up Multimodal Emotion Recognition Pipeline ===")
    print()
    
    # Install required packages
    print("Installing required packages...")
    
    import subprocess
    import sys
    
    packages = [
        'librosa',
        'opencv-python',
        'pandas', 
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn',
        'tqdm'
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
    
    # Install ffmpeg
    print("\nInstalling ffmpeg...")
    try:
        subprocess.run(['apt', 'update'], capture_output=True)
        subprocess.run(['apt', 'install', '-y', 'ffmpeg'], capture_output=True)
        print("✓ ffmpeg installed successfully")
    except:
        print("✗ Failed to install ffmpeg")
    
    print("\n=== Setup completed! ===")
    print("You can now run the audio extraction pipeline.")

if __name__ == "__main__":
    setup_colab_environment()