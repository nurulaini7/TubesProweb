#!/usr/bin/env python3
"""
Demo Lengkap - Multimodal Emotion Recognition Pipeline
dengan Video Download dari Link

Demo ini menunjukkan cara menggunakan pipeline lengkap mulai dari:
1. Download video dari link (Instagram, Drive, YouTube, etc.)
2. Ekstraksi fitur audio
3. Analisis hasil

Author: Assistant
"""

import os
import pandas as pd
import numpy as np
from audio_extraction_pipeline import DatasetProcessor
from video_downloader import VideoDownloader

def create_sample_dataset():
    """Membuat sample dataset untuk demo"""
    sample_data = {
        'id': ['001', '002', '003', '004', '005'],
        'video': [
            'https://drive.google.com/file/d/1abc123/view',  # Google Drive example
            'https://www.instagram.com/reel/ABC123/',        # Instagram Reel example
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',   # YouTube example
            'https://example.com/video.mp4',                 # Direct URL example
            'https://drive.google.com/file/d/1def456/view'   # Another Drive example
        ],
        'emotion': ['Joy', 'Sad', 'Anger', 'Fear', 'Neutral']
    }
    
    df = pd.DataFrame(sample_data)
    csv_path = '/content/sample_datatrain.csv'
    df.to_csv(csv_path, index=False)
    
    print(f"Sample dataset created: {csv_path}")
    print("Dataset contents:")
    print(df)
    print()
    
    return csv_path

def demo_download_only():
    """Demo: Download video saja tanpa processing"""
    print("=== DEMO 1: Download Videos Only ===")
    print()
    
    # Create sample dataset
    csv_path = create_sample_dataset()
    
    # Initialize downloader
    downloader = VideoDownloader(download_dir="/content/demo_videos")
    
    print("Starting video download...")
    downloaded_df = downloader.download_from_csv(
        csv_path=csv_path,
        video_col='video',
        id_col='id',
        max_downloads=3  # Download first 3 videos
    )
    
    if downloaded_df is not None:
        print("\\nDownload completed!")
        print("Download status:")
        print(downloaded_df[['id', 'emotion', 'download_status', 'local_path']])
        
        # Show download statistics
        downloader.print_download_stats()
        
        return downloaded_df
    else:
        print("Download failed!")
        return None

def demo_complete_pipeline():
    """Demo: Pipeline lengkap dengan download otomatis"""
    print("\\n=== DEMO 2: Complete Pipeline with Auto Download ===")
    print()
    
    # Create sample dataset
    csv_path = create_sample_dataset()
    
    # Initialize processor with download enabled
    processor = DatasetProcessor(
        video_dir="/content/demo_videos_complete",
        output_dir="/content/demo_processed",
        enable_download=True  # Enable automatic download
    )
    
    print("Starting complete pipeline (download + processing)...")
    processed_df = processor.process_dataset(
        csv_path=csv_path,
        max_videos=2,  # Process 2 videos
        max_segments_per_video=5,  # Max 5 segments per video
        download_videos=True,  # Enable download
        max_downloads=2  # Download max 2 videos
    )
    
    if processed_df is not None:
        print("\\nPipeline completed!")
        print(f"Total segments processed: {len(processed_df)}")
        print(f"Videos processed: {processed_df['video_id'].nunique()}")
        
        # Show sample results
        print("\\nSample results:")
        sample_cols = ['segment_id', 'video_id', 'timestamp', 'label', 'faces_detected']
        audio_cols = [col for col in processed_df.columns if col.startswith('audio_')][:5]
        display_cols = sample_cols + audio_cols
        print(processed_df[display_cols].head())
        
        # Show emotion distribution
        print("\\nEmotion distribution:")
        print(processed_df['label'].value_counts())
        
        return processed_df
    else:
        print("Processing failed!")
        return None

def demo_manual_process():
    """Demo: Processing video yang sudah di-download manual"""
    print("\\n=== DEMO 3: Process Pre-downloaded Videos ===")
    print()
    
    # Simulasi CSV dengan local files
    manual_data = {
        'id': ['manual_001', 'manual_002'],
        'video': ['local_video1.mp4', 'local_video2.mp4'],  # Local filenames
        'emotion': ['Happy', 'Sad']
    }
    
    manual_df = pd.DataFrame(manual_data)
    manual_csv = '/content/manual_datatrain.csv'
    manual_df.to_csv(manual_csv, index=False)
    
    print("Processing pre-downloaded videos...")
    print("Note: This demo assumes you have manually uploaded videos to /content/manual_videos/")
    
    # Initialize processor without download
    processor = DatasetProcessor(
        video_dir="/content/manual_videos",
        output_dir="/content/manual_processed",
        enable_download=False  # Disable download
    )
    
    print("Manual dataset created:")
    print(manual_df)
    print()
    print("To use this mode:")
    print("1. Upload your videos to /content/manual_videos/")
    print("2. Name them according to the 'id' column (e.g., manual_001.mp4)")
    print("3. Run: processor.process_dataset(csv_path, download_videos=False)")

def demo_retry_failed():
    """Demo: Retry failed downloads"""
    print("\\n=== DEMO 4: Retry Failed Downloads ===")
    print()
    
    # This would typically be run after a previous download attempt
    csv_path = create_sample_dataset()
    
    downloader = VideoDownloader(download_dir="/content/retry_demo")
    
    # First attempt (some might fail due to network issues, invalid URLs, etc.)
    print("First download attempt...")
    df = downloader.download_from_csv(csv_path, max_downloads=5)
    
    if df is not None:
        # Check for failed downloads
        failed_df = downloader.get_failed_downloads(df)
        
        if len(failed_df) > 0:
            print(f"\\nFound {len(failed_df)} failed downloads:")
            print(failed_df[['id', 'video', 'download_status']])
            
            print("\\nRetrying failed downloads...")
            updated_df = downloader.retry_failed_downloads(df)
            
            print("\\nAfter retry:")
            print(updated_df[['id', 'download_status', 'local_path']])
        else:
            print("\\nNo failed downloads to retry!")
    
    return df

def demo_analyze_results(processed_df):
    """Demo: Analisis hasil processing"""
    if processed_df is None:
        print("No data to analyze")
        return
    
    print("\\n=== DEMO 5: Analyze Results ===")
    print()
    
    # Basic statistics
    print("Basic Statistics:")
    print(f"  Total segments: {len(processed_df)}")
    print(f"  Unique videos: {processed_df['video_id'].nunique()}")
    print(f"  Average segments per video: {len(processed_df) / processed_df['video_id'].nunique():.1f}")
    print(f"  Total faces detected: {processed_df['faces_detected'].sum()}")
    print(f"  Average faces per segment: {processed_df['faces_detected'].mean():.1f}")
    
    # Feature statistics
    audio_cols = [col for col in processed_df.columns if col.startswith('audio_')]
    print(f"\\nFeature Statistics:")
    print(f"  Total audio features: {len(audio_cols)}")
    print(f"  MFCC features: {len([col for col in audio_cols if 'mfcc' in col])}")
    print(f"  Chroma features: {len([col for col in audio_cols if 'chroma' in col])}")
    print(f"  Spectral Contrast features: {len([col for col in audio_cols if 'contrast' in col])}")
    print(f"  ZCR features: {len([col for col in audio_cols if 'zcr' in col])}")
    
    # Emotion distribution
    print(f"\\nEmotion Distribution:")
    emotion_counts = processed_df['label'].value_counts()
    for emotion, count in emotion_counts.items():
        percentage = count / len(processed_df) * 100
        print(f"  {emotion}: {count} segments ({percentage:.1f}%)")
    
    # Sample feature values
    print(f"\\nSample Feature Values (first segment):")
    first_segment = processed_df.iloc[0]
    sample_features = [col for col in audio_cols[:10]]  # First 10 features
    for feature in sample_features:
        print(f"  {feature}: {first_segment[feature]:.4f}")
    
    # Save analysis results
    output_path = "/content/analysis_results.csv"
    
    # Create summary dataframe
    summary_data = {
        'metric': ['total_segments', 'unique_videos', 'avg_segments_per_video', 
                  'total_faces', 'avg_faces_per_segment', 'total_features'],
        'value': [len(processed_df), processed_df['video_id'].nunique(),
                 len(processed_df) / processed_df['video_id'].nunique(),
                 processed_df['faces_detected'].sum(), processed_df['faces_detected'].mean(),
                 len(audio_cols)]
    }
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(output_path.replace('.csv', '_summary.csv'), index=False)
    
    print(f"\\nAnalysis summary saved to: {output_path.replace('.csv', '_summary.csv')}")

def main():
    """Run all demos"""
    print("🎬 MULTIMODAL EMOTION RECOGNITION - COMPLETE PIPELINE DEMO")
    print("=" * 60)
    print()
    print("This demo shows the complete pipeline from video URLs to audio features.")
    print("Note: Some downloads may fail due to invalid URLs in the sample data.")
    print()
    
    # Run demos
    try:
        # Demo 1: Download only
        downloaded_df = demo_download_only()
        
        # Demo 2: Complete pipeline
        processed_df = demo_complete_pipeline()
        
        # Demo 3: Manual processing info
        demo_manual_process()
        
        # Demo 4: Retry failed downloads
        demo_retry_failed()
        
        # Demo 5: Analyze results
        if processed_df is not None:
            demo_analyze_results(processed_df)
        
        print("\\n" + "=" * 60)
        print("🎉 Demo completed!")
        print()
        print("Next steps for your actual data:")
        print("1. Prepare your CSV with columns: 'id', 'video' (URLs), 'emotion'")
        print("2. Upload the CSV to Google Colab")
        print("3. Run the pipeline:")
        print()
        print("   processor = DatasetProcessor('/content/videos', '/content/processed')")
        print("   df = processor.process_dataset('your_data.csv', download_videos=True)")
        print()
        print("The pipeline supports:")
        print("- ✅ Instagram Reels")
        print("- ✅ Google Drive links") 
        print("- ✅ YouTube videos")
        print("- ✅ Direct video URLs")
        print("- ✅ Multiple Instance Learning (MIL) approach")
        print("- ✅ 99 audio features per segment")
        
    except Exception as e:
        print(f"Demo error: {e}")
        print("This is normal for demo data with fake URLs.")
        print("The pipeline will work correctly with real video URLs.")

if __name__ == "__main__":
    main()