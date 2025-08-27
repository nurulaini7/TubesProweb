#!/usr/bin/env python3
"""
Complete Setup Script untuk Google Colab - Multimodal Emotion Recognition
Audio Feature Extraction Pipeline dengan Video Download

Jalankan script ini di Google Colab untuk setup lengkap termasuk video downloader
"""

import subprocess
import sys
import os

def install_package(package_name, import_name=None):
    """Install package dengan error handling"""
    try:
        if import_name:
            __import__(import_name)
            print(f"✓ {package_name} already installed")
            return True
    except ImportError:
        pass
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name], 
                            capture_output=True, text=True)
        print(f"✓ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package_name}: {e}")
        return False

def install_system_package(package_name):
    """Install system package dengan apt"""
    try:
        # Update package list
        subprocess.run(['apt', 'update'], capture_output=True, text=True)
        
        # Install package
        result = subprocess.run(['apt', 'install', '-y', package_name], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ {package_name} installed successfully")
            return True
        else:
            print(f"✗ Failed to install {package_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error installing {package_name}: {e}")
        return False

def setup_complete_environment():
    """Setup lengkap environment untuk pipeline"""
    
    print("=== Complete Setup for Multimodal Emotion Recognition Pipeline ===")
    print("This will install all required packages for audio extraction AND video download")
    print()
    
    # 1. Install basic packages
    print("--- Step 1: Installing Basic Python Packages ---")
    basic_packages = [
        ('librosa', 'librosa'),
        ('opencv-python', 'cv2'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('scipy', 'scipy'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('tqdm', 'tqdm'),
        ('requests', 'requests')
    ]
    
    basic_success = 0
    for package, import_name in basic_packages:
        if install_package(package, import_name):
            basic_success += 1
    
    print(f"Basic packages: {basic_success}/{len(basic_packages)} installed successfully")
    print()
    
    # 2. Install system packages
    print("--- Step 2: Installing System Packages ---")
    system_packages = ['ffmpeg']
    
    system_success = 0
    for package in system_packages:
        if install_system_package(package):
            system_success += 1
    
    print(f"System packages: {system_success}/{len(system_packages)} installed successfully")
    print()
    
    # 3. Install video download packages
    print("--- Step 3: Installing Video Download Packages ---")
    download_packages = [
        'yt-dlp',
        'gdown',
        'youtube-dl'
    ]
    
    download_success = 0
    for package in download_packages:
        if install_package(package):
            download_success += 1
    
    print(f"Video download packages: {download_success}/{len(download_packages)} installed successfully")
    print()
    
    # 4. Test installations
    print("--- Step 4: Testing Installations ---")
    test_results = []
    
    # Test librosa
    try:
        import librosa
        print(f"✓ librosa {librosa.__version__} working")
        test_results.append(True)
    except:
        print("✗ librosa not working")
        test_results.append(False)
    
    # Test OpenCV
    try:
        import cv2
        print(f"✓ OpenCV {cv2.__version__} working")
        test_results.append(True)
    except:
        print("✗ OpenCV not working")
        test_results.append(False)
    
    # Test ffmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ ffmpeg working")
            test_results.append(True)
        else:
            print("✗ ffmpeg not working")
            test_results.append(False)
    except:
        print("✗ ffmpeg not found")
        test_results.append(False)
    
    # Test yt-dlp
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ yt-dlp {version} working")
            test_results.append(True)
        else:
            print("✗ yt-dlp not working")
            test_results.append(False)
    except:
        print("✗ yt-dlp not found")
        test_results.append(False)
    
    # Test gdown
    try:
        import gdown
        print(f"✓ gdown working")
        test_results.append(True)
    except:
        print("✗ gdown not working")
        test_results.append(False)
    
    print()
    print(f"Test results: {sum(test_results)}/{len(test_results)} components working")
    print()
    
    # 5. Create directories
    print("--- Step 5: Creating Directories ---")
    directories = [
        '/content/videos',
        '/content/processed_data',
        '/content/downloaded_data'
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Created directory: {directory}")
        except Exception as e:
            print(f"✗ Failed to create directory {directory}: {e}")
    
    print()
    
    # 6. Download pipeline files (if not already present)
    print("--- Step 6: Setting up Pipeline Files ---")
    
    # Create sample usage script
    sample_code = '''
# =================================================================
# SAMPLE USAGE - Multimodal Emotion Recognition Pipeline
# =================================================================

# 1. Import the pipeline
from audio_extraction_pipeline import DatasetProcessor
from video_downloader import VideoDownloader

# 2. Setup paths
VIDEO_DIR = "/content/videos"
CSV_PATH = "/content/datatrain.csv"  # Upload your CSV here
OUTPUT_DIR = "/content/processed_data"

# 3. Initialize processor with download enabled
processor = DatasetProcessor(
    video_dir=VIDEO_DIR, 
    output_dir=OUTPUT_DIR, 
    enable_download=True  # Enable automatic video download
)

# 4. Process dataset (with automatic download)
processed_df = processor.process_dataset(
    csv_path=CSV_PATH,
    max_videos=5,  # Start with 5 videos for testing
    max_segments_per_video=10,  # Max 10 segments per video
    download_videos=True,  # Enable download
    max_downloads=5  # Download max 5 videos
)

# 5. Check results
if processed_df is not None:
    print(f"Successfully processed {len(processed_df)} segments")
    print(f"From {processed_df['video_id'].nunique()} unique videos")
    print(f"Emotion distribution:")
    print(processed_df['label'].value_counts())

# 6. Save results
if processed_df is not None:
    output_file = "/content/processed_audio_features.csv"
    processed_df.to_csv(output_file, index=False)
    print(f"Results saved to: {output_file}")

# =================================================================
# DOWNLOAD ONLY MODE (if you just want to download videos first)
# =================================================================

# Option 1: Download only
downloader = VideoDownloader(download_dir="/content/videos")
downloaded_df = downloader.download_from_csv(
    csv_path="/content/datatrain.csv",
    max_downloads=10
)

# Option 2: Process without download (videos already downloaded)
processor_no_download = DatasetProcessor(
    video_dir=VIDEO_DIR,
    output_dir=OUTPUT_DIR,
    enable_download=False  # Disable download
)

processed_df = processor_no_download.process_dataset(
    csv_path=CSV_PATH,
    download_videos=False  # Process existing videos only
)
'''
    
    try:
        with open('/content/sample_usage.py', 'w') as f:
            f.write(sample_code)
        print("✓ Created sample usage script: /content/sample_usage.py")
    except Exception as e:
        print(f"✗ Failed to create sample script: {e}")
    
    print()
    
    # 7. Final summary
    print("=== Setup Summary ===")
    print()
    print("✓ Environment setup completed!")
    print()
    print("Next steps:")
    print("1. Upload your datatrain.csv file to /content/")
    print("2. Make sure your CSV has columns: 'id', 'video' (URLs), 'emotion'")
    print("3. Run the pipeline:")
    print()
    print("   # Import and setup")
    print("   from audio_extraction_pipeline import DatasetProcessor")
    print("   processor = DatasetProcessor('/content/videos', '/content/processed_data')")
    print()
    print("   # Process with automatic download")
    print("   df = processor.process_dataset(")
    print("       csv_path='/content/datatrain.csv',")
    print("       max_videos=5,  # Start small")
    print("       download_videos=True")
    print("   )")
    print()
    print("Supported video sources:")
    print("- Instagram Reels")
    print("- Google Drive links")
    print("- YouTube videos")
    print("- Direct video URLs")
    print()
    print("Pipeline will automatically:")
    print("1. Download videos from URLs in your CSV")
    print("2. Detect faces in video frames")
    print("3. Extract audio segments around face timestamps")
    print("4. Extract 99 audio features (MFCC, Chroma, Spectral Contrast, ZCR)")
    print("5. Save processed dataset as CSV")
    print()
    
    return sum(test_results) >= len(test_results) * 0.8  # 80% success rate

if __name__ == "__main__":
    success = setup_complete_environment()
    if success:
        print("🎉 Setup completed successfully!")
    else:
        print("⚠️  Setup completed with some issues. Check the output above.")