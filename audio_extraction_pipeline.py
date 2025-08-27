#!/usr/bin/env python3
"""
Multimodal Emotion Recognition - Audio Feature Extraction Pipeline

Pipeline untuk ekstraksi fitur audio dari video sebagai bagian dari sistem MER 
dengan pendekatan Multiple Instance Learning (MIL).

Author: Assistant
Created for: Google Colab Environment
"""

import os
import pandas as pd
import numpy as np
import librosa
import cv2
import subprocess
from scipy import stats
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Import video downloader
try:
    from video_downloader import VideoDownloader
    DOWNLOADER_AVAILABLE = True
except ImportError:
    DOWNLOADER_AVAILABLE = False
    print("Warning: VideoDownloader not available. Videos must be downloaded manually.")

class AudioExtractor:
    """
    Class untuk ekstraksi audio dari video menggunakan ffmpeg
    """
    
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
    
    def extract_audio_from_video(self, video_path, output_path=None, start_time=None, duration=None):
        """
        Ekstrak audio dari video menggunakan ffmpeg
        
        Args:
            video_path (str): Path ke file video
            output_path (str): Path output file audio (optional)
            start_time (float): Waktu mulai dalam detik (optional)
            duration (float): Durasi dalam detik (optional)
        
        Returns:
            str: Path ke file audio yang diekstrak
        """
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = f"{base_name}_audio.wav"
        
        # Build ffmpeg command
        cmd = ['ffmpeg', '-i', video_path, '-y']
        
        # Add time constraints if specified
        if start_time is not None:
            cmd.extend(['-ss', str(start_time)])
        if duration is not None:
            cmd.extend(['-t', str(duration)])
        
        # Audio extraction parameters
        cmd.extend([
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # Audio codec
            '-ar', str(self.sample_rate),  # Sample rate
            '-ac', '1',  # Mono channel
            output_path
        ])
        
        try:
            # Execute ffmpeg command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"Audio extracted successfully: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Error extracting audio: {e}")
            print(f"Command: {' '.join(cmd)}")
            print(f"Error output: {e.stderr}")
            return None
    
    def load_audio_segment(self, audio_path, start_time=None, duration=None):
        """
        Load audio segment menggunakan librosa
        
        Args:
            audio_path (str): Path ke file audio
            start_time (float): Waktu mulai dalam detik
            duration (float): Durasi dalam detik
        
        Returns:
            tuple: (audio_data, sample_rate)
        """
        try:
            offset = start_time if start_time is not None else 0
            y, sr = librosa.load(audio_path, sr=self.sample_rate, offset=offset, duration=duration)
            return y, sr
        except Exception as e:
            print(f"Error loading audio segment: {e}")
            return None, None

class AudioFeatureExtractor:
    """
    Class untuk ekstraksi fitur audio: MFCC, Chroma, Spectral Contrast, Zero Crossing Rate
    """
    
    def __init__(self, sample_rate=22050, n_mfcc=13, n_chroma=12):
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
        self.n_chroma = n_chroma
    
    def extract_mfcc(self, audio_data):
        """
        Ekstrak MFCC features
        
        Args:
            audio_data (np.array): Audio time series
        
        Returns:
            np.array: MFCC features
        """
        try:
            mfcc = librosa.feature.mfcc(y=audio_data, sr=self.sample_rate, n_mfcc=self.n_mfcc)
            return mfcc
        except Exception as e:
            print(f"Error extracting MFCC: {e}")
            return np.zeros((self.n_mfcc, 1))
    
    def extract_chroma(self, audio_data):
        """
        Ekstrak Chroma features
        
        Args:
            audio_data (np.array): Audio time series
        
        Returns:
            np.array: Chroma features
        """
        try:
            chroma = librosa.feature.chroma_stft(y=audio_data, sr=self.sample_rate, n_chroma=self.n_chroma)
            return chroma
        except Exception as e:
            print(f"Error extracting Chroma: {e}")
            return np.zeros((self.n_chroma, 1))
    
    def extract_spectral_contrast(self, audio_data):
        """
        Ekstrak Spectral Contrast features
        
        Args:
            audio_data (np.array): Audio time series
        
        Returns:
            np.array: Spectral contrast features
        """
        try:
            spectral_contrast = librosa.feature.spectral_contrast(y=audio_data, sr=self.sample_rate)
            return spectral_contrast
        except Exception as e:
            print(f"Error extracting Spectral Contrast: {e}")
            return np.zeros((7, 1))  # Default 7 bands
    
    def extract_zero_crossing_rate(self, audio_data):
        """
        Ekstrak Zero Crossing Rate
        
        Args:
            audio_data (np.array): Audio time series
        
        Returns:
            np.array: Zero crossing rate
        """
        try:
            zcr = librosa.feature.zero_crossing_rate(audio_data)
            return zcr
        except Exception as e:
            print(f"Error extracting ZCR: {e}")
            return np.zeros((1, 1))
    
    def compute_statistics(self, features):
        """
        Compute statistical measures (mean, std, skewness) for features
        
        Args:
            features (np.array): Feature matrix (features x time_frames)
        
        Returns:
            np.array: Statistical features [mean, std, skewness] for each feature
        """
        try:
            if features.size == 0:
                return np.zeros(3)  # Return zeros if empty
            
            # Compute statistics across time dimension
            mean_vals = np.mean(features, axis=1)
            std_vals = np.std(features, axis=1)
            skew_vals = stats.skew(features, axis=1)
            
            # Handle NaN values
            mean_vals = np.nan_to_num(mean_vals)
            std_vals = np.nan_to_num(std_vals)
            skew_vals = np.nan_to_num(skew_vals)
            
            # Concatenate all statistics
            stats_features = np.concatenate([mean_vals, std_vals, skew_vals])
            return stats_features
        except Exception as e:
            print(f"Error computing statistics: {e}")
            return np.zeros(features.shape[0] * 3)
    
    def extract_all_features(self, audio_data):
        """
        Ekstrak semua fitur audio dan gabungkan menjadi satu vektor
        
        Args:
            audio_data (np.array): Audio time series
        
        Returns:
            np.array: Combined feature vector
        """
        if len(audio_data) == 0:
            # Return zero vector if audio is empty
            total_features = (self.n_mfcc + self.n_chroma + 7 + 1) * 3  # 3 statistics per feature
            return np.zeros(total_features)
        
        # Extract all features
        mfcc = self.extract_mfcc(audio_data)
        chroma = self.extract_chroma(audio_data)
        spectral_contrast = self.extract_spectral_contrast(audio_data)
        zcr = self.extract_zero_crossing_rate(audio_data)
        
        # Compute statistics for each feature type
        mfcc_stats = self.compute_statistics(mfcc)
        chroma_stats = self.compute_statistics(chroma)
        contrast_stats = self.compute_statistics(spectral_contrast)
        zcr_stats = self.compute_statistics(zcr)
        
        # Combine all features
        combined_features = np.concatenate([
            mfcc_stats,
            chroma_stats,
            contrast_stats,
            zcr_stats
        ])
        
        return combined_features
    
    def get_feature_names(self):
        """
        Get feature names for the combined feature vector
        
        Returns:
            list: List of feature names
        """
        feature_names = []
        
        # MFCC feature names
        for i in range(self.n_mfcc):
            feature_names.extend([f'mfcc_{i}_mean', f'mfcc_{i}_std', f'mfcc_{i}_skew'])
        
        # Chroma feature names
        for i in range(self.n_chroma):
            feature_names.extend([f'chroma_{i}_mean', f'chroma_{i}_std', f'chroma_{i}_skew'])
        
        # Spectral contrast feature names
        for i in range(7):  # Default 7 bands
            feature_names.extend([f'contrast_{i}_mean', f'contrast_{i}_std', f'contrast_{i}_skew'])
        
        # ZCR feature names
        feature_names.extend(['zcr_mean', 'zcr_std', 'zcr_skew'])
        
        return feature_names

class VideoFrameDetector:
    """
    Class untuk deteksi frame dengan wajah menggunakan Haar Cascade
    """
    
    def __init__(self, fps_extract=2):
        self.fps_extract = fps_extract  # Extract 2 frames per second
        
        # Load Haar Cascade for face detection
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            print("Haar Cascade loaded successfully!")
        except Exception as e:
            print(f"Error loading Haar Cascade: {e}")
            self.face_cascade = None
    
    def detect_faces_in_frame(self, frame):
        """
        Deteksi wajah dalam frame
        
        Args:
            frame (np.array): Video frame
        
        Returns:
            list: List of face bounding boxes
        """
        if self.face_cascade is None:
            return []
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            return faces
        except Exception as e:
            print(f"Error detecting faces: {e}")
            return []
    
    def extract_frames_with_faces(self, video_path, max_frames=None):
        """
        Ekstrak frame dari video yang mengandung wajah
        
        Args:
            video_path (str): Path ke file video
            max_frames (int): Maximum number of frames to extract
        
        Returns:
            list: List of dictionaries containing frame info
        """
        frames_with_faces = []
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                print(f"Error opening video: {video_path}")
                return frames_with_faces
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            print(f"Video info: {fps:.2f} FPS, {total_frames} frames, {duration:.2f}s")
            
            # Calculate frame interval for extraction
            frame_interval = int(fps / self.fps_extract) if fps > 0 else 1
            
            frame_count = 0
            extracted_count = 0
            
            with tqdm(total=total_frames, desc="Processing frames") as pbar:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Extract frames at specified interval
                    if frame_count % frame_interval == 0:
                        faces = self.detect_faces_in_frame(frame)
                        
                        if len(faces) > 0:
                            timestamp = frame_count / fps if fps > 0 else frame_count
                            
                            frame_info = {
                                'frame_id': f"{os.path.splitext(os.path.basename(video_path))[0]}_frame_{frame_count:06d}",
                                'timestamp': timestamp,
                                'frame_number': frame_count,
                                'faces_detected': len(faces),
                                'frame_data': frame.copy()
                            }
                            
                            frames_with_faces.append(frame_info)
                            extracted_count += 1
                            
                            # Check max_frames limit
                            if max_frames and extracted_count >= max_frames:
                                break
                    
                    frame_count += 1
                    pbar.update(1)
            
            cap.release()
            print(f"Extracted {extracted_count} frames with faces from {total_frames} total frames")
            
        except Exception as e:
            print(f"Error processing video: {e}")
        
        return frames_with_faces

class DatasetProcessor:
    """
    Class untuk memproses dataset dan menggabungkan semua komponen
    """
    
    def __init__(self, video_dir, output_dir="processed_data", enable_download=True):
        self.video_dir = video_dir
        self.output_dir = output_dir
        self.enable_download = enable_download
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(video_dir, exist_ok=True)
        
        # Initialize components
        self.audio_extractor = AudioExtractor()
        self.feature_extractor = AudioFeatureExtractor()
        self.frame_detector = VideoFrameDetector()
        
        # Initialize video downloader if available and enabled
        if enable_download and DOWNLOADER_AVAILABLE:
            self.video_downloader = VideoDownloader(download_dir=video_dir)
            print(f"DatasetProcessor initialized with video downloader enabled")
        else:
            self.video_downloader = None
            if enable_download:
                print("Video downloader not available - videos must be pre-downloaded")
        
        print(f"DatasetProcessor initialized with output directory: {output_dir}")
    
    def load_dataset(self, csv_path):
        """
        Load dataset dari CSV file
        
        Args:
            csv_path (str): Path ke file CSV dataset
        
        Returns:
            pd.DataFrame: Dataset
        """
        try:
            df = pd.read_csv(csv_path)
            print(f"Dataset loaded successfully: {len(df)} entries")
            print(f"Columns: {list(df.columns)}")
            
            # Check required columns
            required_cols = ['id', 'video', 'emotion']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                print(f"Warning: Missing required columns: {missing_cols}")
                print("Expected columns: 'id' (video ID), 'video' (URL), 'emotion' (label)")
            
            return df
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return None
    
    def download_videos_from_dataset(self, csv_path, max_downloads=None, video_col='video', id_col='id'):
        """
        Download semua video dari dataset CSV
        
        Args:
            csv_path (str): Path ke file CSV dataset
            max_downloads (int): Maksimal jumlah download (None = unlimited)
            video_col (str): Nama kolom yang berisi URL video
            id_col (str): Nama kolom yang berisi ID video
        
        Returns:
            pd.DataFrame: Updated dataframe dengan kolom 'local_path'
        """
        if not self.video_downloader:
            print("Error: Video downloader not available")
            return None
        
        print(f"Starting video download from {csv_path}")
        print(f"Max downloads: {'Unlimited' if max_downloads is None else max_downloads}")
        
        # Download videos
        df_with_downloads = self.video_downloader.download_from_csv(
            csv_path=csv_path,
            video_col=video_col,
            id_col=id_col,
            max_downloads=max_downloads
        )
        
        return df_with_downloads
    
    def get_video_path(self, df, video_id):
        """
        Get local video path untuk video ID tertentu
        
        Args:
            df (pd.DataFrame): Dataset dengan kolom local_path
            video_id (str): ID video
        
        Returns:
            str: Path ke file video lokal, atau None jika tidak ada
        """
        if 'local_path' in df.columns:
            # Cari berdasarkan downloaded videos
            video_row = df[df['id'] == video_id]
            if len(video_row) > 0 and pd.notna(video_row.iloc[0]['local_path']):
                local_path = video_row.iloc[0]['local_path']
                if os.path.exists(local_path):
                    return local_path
        
        # Fallback: cari file dengan nama video_id
        possible_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        for ext in possible_extensions:
            video_path = os.path.join(self.video_dir, f"{video_id}{ext}")
            if os.path.exists(video_path):
                return video_path
        
        return None
    
    def process_single_video(self, video_path, video_id, emotion_label, max_segments=None):
        """
        Proses satu video untuk ekstraksi fitur audio
        
        Args:
            video_path (str): Path ke file video
            video_id (str): ID video
            emotion_label (str): Label emosi
            max_segments (int): Maximum number of segments to process
        
        Returns:
            list: List of processed segments
        """
        segments = []
        
        print(f"\nProcessing video: {video_id}")
        
        try:
            # Step 1: Extract frames with faces
            frames_with_faces = self.frame_detector.extract_frames_with_faces(
                video_path, max_frames=max_segments
            )
            
            if len(frames_with_faces) == 0:
                print(f"No faces detected in video: {video_id}")
                return segments
            
            # Step 2: Extract full audio from video
            audio_path = os.path.join(self.output_dir, f"{video_id}_audio.wav")
            extracted_audio = self.audio_extractor.extract_audio_from_video(
                video_path, audio_path
            )
            
            if extracted_audio is None:
                print(f"Failed to extract audio from video: {video_id}")
                return segments
            
            # Step 3: Process each frame timestamp
            for frame_info in tqdm(frames_with_faces, desc=f"Processing {video_id} segments"):
                try:
                    timestamp = frame_info['timestamp']
                    frame_id = frame_info['frame_id']
                    
                    # Extract audio segment around frame timestamp (±1 second)
                    segment_duration = 2.0  # 2 seconds total
                    start_time = max(0, timestamp - 1.0)  # 1 second before
                    
                    audio_data, sr = self.audio_extractor.load_audio_segment(
                        audio_path, start_time, segment_duration
                    )
                    
                    if audio_data is not None and len(audio_data) > 0:
                        # Extract audio features
                        audio_features = self.feature_extractor.extract_all_features(audio_data)
                        
                        # Create segment data
                        segment_data = {
                            'segment_id': f"{video_id}_seg_{len(segments):03d}",
                            'video_id': video_id,
                            'frame_id': frame_id,
                            'timestamp': f"{timestamp:.2f}",
                            'audio_features': audio_features.tolist(),
                            'label': emotion_label,
                            'faces_detected': frame_info['faces_detected']
                        }
                        
                        segments.append(segment_data)
                    
                except Exception as e:
                    print(f"Error processing frame {frame_id}: {e}")
                    continue
            
            # Clean up audio file
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            print(f"Successfully processed {len(segments)} segments from {video_id}")
            
        except Exception as e:
            print(f"Error processing video {video_id}: {e}")
        
        return segments
    
    def process_dataset(self, csv_path, max_videos=None, max_segments_per_video=None, 
                       download_videos=True, max_downloads=None):
        """
        Proses seluruh dataset dengan opsi download otomatis
        
        Args:
            csv_path (str): Path ke file CSV dataset
            max_videos (int): Maximum number of videos to process
            max_segments_per_video (int): Maximum segments per video
            download_videos (bool): Apakah download video otomatis
            max_downloads (int): Maximum number of videos to download
        
        Returns:
            pd.DataFrame: Processed dataset
        """
        print(f"=== Starting Dataset Processing ===")
        print(f"CSV path: {csv_path}")
        print(f"Max videos to process: {max_videos or 'All'}")
        print(f"Max segments per video: {max_segments_per_video or 'All'}")
        print(f"Download videos: {download_videos}")
        
        # Step 1: Download videos if enabled
        if download_videos and self.video_downloader:
            print(f"\n--- Step 1: Downloading Videos ---")
            df = self.download_videos_from_dataset(
                csv_path=csv_path,
                max_downloads=max_downloads or max_videos,
                video_col='video',
                id_col='id'
            )
            
            if df is None:
                print("Failed to download videos")
                return None
            
            # Save updated CSV with download info
            download_csv_path = csv_path.replace('.csv', '_with_downloads.csv')
            df.to_csv(download_csv_path, index=False)
            print(f"Updated CSV saved: {download_csv_path}")
            
        else:
            print(f"\n--- Step 1: Loading Dataset (No Download) ---")
            df = self.load_dataset(csv_path)
            if df is None:
                return None
        
        # Step 2: Process videos for feature extraction
        print(f"\n--- Step 2: Processing Videos for Feature Extraction ---")
        
        all_segments = []
        processed_videos = 0
        skipped_videos = 0
        
        for idx, row in df.iterrows():
            if max_videos and processed_videos >= max_videos:
                break
            
            try:
                video_id = str(row['id'])
                emotion_label = str(row['emotion'])
                
                # Get video path (try downloaded path first, then fallback)
                video_path = self.get_video_path(df, video_id)
                
                if not video_path:
                    print(f"Video file not found for ID: {video_id}")
                    skipped_videos += 1
                    continue
                
                print(f"\nProcessing video {processed_videos + 1}: {video_id}")
                print(f"  Path: {video_path}")
                print(f"  Emotion: {emotion_label}")
                
                # Process video
                segments = self.process_single_video(
                    video_path, video_id, emotion_label, max_segments_per_video
                )
                
                all_segments.extend(segments)
                processed_videos += 1
                
                print(f"✓ Processed {len(segments)} segments from {video_id}")
                print(f"Progress: {processed_videos}/{min(len(df), max_videos or len(df))} videos processed")
                
            except Exception as e:
                print(f"✗ Error processing video {video_id}: {e}")
                skipped_videos += 1
                continue
        
        # Convert to DataFrame
        if all_segments:
            # Flatten audio features for CSV
            feature_names = self.feature_extractor.get_feature_names()
            
            processed_data = []
            for segment in all_segments:
                row_data = {
                    'segment_id': segment['segment_id'],
                    'video_id': segment['video_id'],
                    'frame_id': segment['frame_id'],
                    'timestamp': segment['timestamp'],
                    'label': segment['label'],
                    'faces_detected': segment['faces_detected']
                }
                
                # Add audio features
                for i, feature_name in enumerate(feature_names):
                    if i < len(segment['audio_features']):
                        row_data[f'audio_{feature_name}'] = segment['audio_features'][i]
                    else:
                        row_data[f'audio_{feature_name}'] = 0.0
                
                processed_data.append(row_data)
            
            result_df = pd.DataFrame(processed_data)
            
            # Save processed dataset
            output_path = os.path.join(self.output_dir, 'processed_audio_features.csv')
            result_df.to_csv(output_path, index=False)
            print(f"\nProcessed dataset saved to: {output_path}")
            print(f"Total segments: {len(result_df)}")
            print(f"Feature columns: {len([col for col in result_df.columns if col.startswith('audio_')])}")
            
            return result_df
        else:
            print("No segments were processed successfully")
            return None

# Utility Functions
def visualize_audio_features(processed_df, sample_size=100):
    """
    Visualisasi distribusi fitur audio
    """
    if processed_df is None or len(processed_df) == 0:
        print("No data to visualize")
        return
    
    # Sample data for visualization
    sample_df = processed_df.sample(min(sample_size, len(processed_df)))
    
    # Get audio feature columns
    audio_cols = [col for col in sample_df.columns if col.startswith('audio_')]
    
    if len(audio_cols) == 0:
        print("No audio features found")
        return
    
    # Plot feature distributions
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # MFCC features
    mfcc_cols = [col for col in audio_cols if 'mfcc' in col][:10]
    if mfcc_cols:
        sample_df[mfcc_cols].hist(bins=20, ax=axes[0,0])
        axes[0,0].set_title('MFCC Features Distribution')
    
    # Chroma features
    chroma_cols = [col for col in audio_cols if 'chroma' in col][:10]
    if chroma_cols:
        sample_df[chroma_cols].hist(bins=20, ax=axes[0,1])
        axes[0,1].set_title('Chroma Features Distribution')
    
    # Spectral contrast features
    contrast_cols = [col for col in audio_cols if 'contrast' in col][:10]
    if contrast_cols:
        sample_df[contrast_cols].hist(bins=20, ax=axes[1,0])
        axes[1,0].set_title('Spectral Contrast Features Distribution')
    
    # ZCR features
    zcr_cols = [col for col in audio_cols if 'zcr' in col]
    if zcr_cols:
        sample_df[zcr_cols].hist(bins=20, ax=axes[1,1])
        axes[1,1].set_title('ZCR Features Distribution')
    
    plt.tight_layout()
    plt.show()
    
    # Label distribution
    plt.figure(figsize=(10, 6))
    sample_df['label'].value_counts().plot(kind='bar')
    plt.title('Emotion Label Distribution')
    plt.xlabel('Emotion')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

def save_feature_summary(processed_df, output_path):
    """
    Save summary statistics fitur audio
    """
    if processed_df is None:
        return
    
    audio_cols = [col for col in processed_df.columns if col.startswith('audio_')]
    
    summary = processed_df[audio_cols].describe()
    summary.to_csv(output_path)
    print(f"Feature summary saved to: {output_path}")

def test_single_video_processing(processor, video_path, video_id="test_video", emotion_label="test"):
    """
    Test processing dengan satu video
    """
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return None
    
    print(f"Testing with video: {video_path}")
    
    # Process single video
    segments = processor.process_single_video(
        video_path, video_id, emotion_label, max_segments=5
    )
    
    if segments:
        print(f"\n=== Test Results ===")
        print(f"Processed segments: {len(segments)}")
        print(f"Feature vector length: {len(segments[0]['audio_features'])}")
        
        # Show first segment details
        first_segment = segments[0]
        print(f"\nFirst segment:")
        print(f"  Segment ID: {first_segment['segment_id']}")
        print(f"  Timestamp: {first_segment['timestamp']}")
        print(f"  Faces detected: {first_segment['faces_detected']}")
        print(f"  Feature vector shape: {np.array(first_segment['audio_features']).shape}")
        
        return segments
    else:
        print("No segments processed")
        return None

# Main function untuk demo
def main():
    """
    Demo function untuk menunjukkan cara penggunaan
    """
    print("=== Multimodal Emotion Recognition - Audio Feature Extraction ===")
    print()
    
    # Konfigurasi paths
    VIDEO_DIR = "/workspace/videos"  # Direktori tempat video disimpan
    CSV_PATH = "/workspace/datatrain.csv"  # Path ke file CSV dataset
    OUTPUT_DIR = "/workspace/processed_data"  # Direktori output
    
    # Buat direktori jika belum ada
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Video directory: {VIDEO_DIR}")
    print(f"CSV path: {CSV_PATH}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()
    
    # Initialize processor
    processor = DatasetProcessor(VIDEO_DIR, OUTPUT_DIR)
    print("Processor initialized successfully!")
    print()
    
    # Instructions
    print("=== Instructions untuk penggunaan ===")
    print("1. Place your videos in the VIDEO_DIR")
    print("2. Update CSV_PATH to point to your datatrain.csv")
    print("3. Run the processing:")
    print()
    print("# Proses dataset (dengan limitasi untuk testing)")
    print("processed_df = processor.process_dataset(")
    print("    csv_path=CSV_PATH,")
    print("    max_videos=5,  # Proses maksimal 5 video untuk testing")
    print("    max_segments_per_video=10  # Maksimal 10 segmen per video")
    print(")")
    print()
    print("# Untuk test dengan single video:")
    print("# test_segments = test_single_video_processing(processor, '/path/to/video.mp4')")
    print()
    
    # Show feature information
    feature_extractor = AudioFeatureExtractor()
    feature_names = feature_extractor.get_feature_names()
    print(f"=== Feature Information ===")
    print(f"Total features per segment: {len(feature_names)}")
    print(f"MFCC features: {len([f for f in feature_names if 'mfcc' in f])}")
    print(f"Chroma features: {len([f for f in feature_names if 'chroma' in f])}")
    print(f"Spectral Contrast features: {len([f for f in feature_names if 'contrast' in f])}")
    print(f"ZCR features: {len([f for f in feature_names if 'zcr' in f])}")
    print()
    
    return processor

if __name__ == "__main__":
    processor = main()