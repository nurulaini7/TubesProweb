# Multimodal Emotion Recognition - Audio Feature Extraction Pipeline

Pipeline lengkap untuk ekstraksi fitur audio dari video dengan **download otomatis** dari berbagai sumber (Instagram Reels, Google Drive, YouTube, dll) sebagai bagian dari sistem MER dengan pendekatan Multiple Instance Learning (MIL).

## 🚀 Features Utama

### ✅ Video Download Otomatis
- **Instagram Reels**: Download langsung dari link Instagram
- **Google Drive**: Support Google Drive sharing links 
- **YouTube**: Download dari YouTube URLs
- **Direct URLs**: Download dari URL video langsung
- **Error Handling**: Retry mechanism dan handling untuk failed downloads

### ✅ Audio Feature Extraction
- **MFCC**: 13 koefisien × 3 statistik = 39 fitur
- **Chroma**: 12 koefisien × 3 statistik = 36 fitur  
- **Spectral Contrast**: 7 band × 3 statistik = 21 fitur
- **Zero Crossing Rate**: 1 × 3 statistik = 3 fitur
- **Total**: **99 fitur audio per segmen**

### ✅ Multiple Instance Learning (MIL)
- Label video sebagai weak supervision untuk segmen
- Deteksi frame dengan wajah menggunakan Haar Cascade (non-pretrained)
- Mapping timestamp audio ke frame yang mengandung wajah

## 📁 Struktur File

```
/workspace/
├── audio_extraction_pipeline.py    # Main pipeline script
├── video_downloader.py             # Video downloader module
├── complete_setup_colab.py         # Complete setup script
├── demo_complete_pipeline.py       # Demo lengkap
├── README.md                       # Dokumentasi ini
└── videos/                         # Direktori untuk video download
```

## Fitur yang Diekstrak

### Audio Features (99 fitur total per segmen):
- **MFCC**: 13 koefisien × 3 statistik (mean, std, skewness) = 39 fitur
- **Chroma**: 12 koefisien × 3 statistik = 36 fitur  
- **Spectral Contrast**: 7 band × 3 statistik = 21 fitur
- **Zero Crossing Rate**: 1 × 3 statistik = 3 fitur

### Statistik yang Dihitung:
- **Mean**: Rata-rata nilai fitur sepanjang waktu
- **Standard Deviation**: Variabilitas fitur 
- **Skewness**: Kemencengan distribusi fitur

## Format Dataset Output

```csv
segment_id,video_id,frame_id,timestamp,label,faces_detected,audio_mfcc_0_mean,audio_mfcc_0_std,audio_mfcc_0_skew,...
vid001_seg001,vid001,vid001_frame_000030,1.50,Joy,2,12.34,-1.23,0.45,...
vid001_seg002,vid001,vid001_frame_000060,3.00,Joy,1,10.12,-0.98,0.33,...
```

## 🔧 Quick Start di Google Colab

### 1. Complete Setup (Recommended)

```python
# Upload files ke Colab atau download dari repository
# Kemudian jalankan setup lengkap:
!python complete_setup_colab.py
```

**Atau setup manual:**

```python
# Install packages untuk audio processing
!pip install librosa opencv-python pandas numpy scipy matplotlib seaborn tqdm

# Install packages untuk video download  
!pip install yt-dlp gdown youtube-dl

# Install system dependencies
!apt update && apt install -y ffmpeg
```

### 2. Import Pipeline dengan Video Downloader

```python
# Import main classes
from audio_extraction_pipeline import DatasetProcessor
from video_downloader import VideoDownloader

print("Pipeline with video downloader ready!")
```

### 3. Setup Directories dan Processor

```python
import os

# Konfigurasi paths
VIDEO_DIR = "/content/videos"
CSV_PATH = "/content/datatrain.csv" 
OUTPUT_DIR = "/content/processed_data"

# Buat direktori
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize processor dengan download enabled
processor = DatasetProcessor(
    video_dir=VIDEO_DIR, 
    output_dir=OUTPUT_DIR,
    enable_download=True  # 🔥 Enable automatic video download
)
```

### 4. Prepare Your Dataset

Buat file CSV dengan format:

```csv
id,video,emotion
001,https://www.instagram.com/reel/ABC123/,Joy
002,https://drive.google.com/file/d/1abc123/view,Sad
003,https://www.youtube.com/watch?v=xyz789,Anger
004,https://example.com/video.mp4,Fear
005,https://drive.google.com/file/d/1def456/view,Neutral
```

```python
# Upload CSV ke Colab
from google.colab import files
uploaded = files.upload()  # Upload your datatrain.csv

# Atau mount Google Drive
from google.colab import drive
drive.mount('/content/drive')
CSV_PATH = '/content/drive/MyDrive/datatrain.csv'
```

### 5. Run Complete Pipeline (Download + Process)

```python
# 🚀 One-command processing dengan auto download
processed_df = processor.process_dataset(
    csv_path=CSV_PATH,
    max_videos=10,           # Process 10 videos
    max_segments_per_video=15,   # Max 15 segments per video
    download_videos=True,        # 🔥 Enable auto download
    max_downloads=10         # Download max 10 videos
)

if processed_df is not None:
    print(f"✅ Successfully processed {len(processed_df)} segments")
    print(f"📁 From {processed_df['video_id'].nunique()} videos")
    print(f"🎭 Emotions: {processed_df['label'].value_counts().to_dict()}")
```

### 6. Alternative: Download Only Mode

```python
# Just download videos first (no processing)
downloader = VideoDownloader(download_dir="/content/videos")

downloaded_df = downloader.download_from_csv(
    csv_path=CSV_PATH,
    max_downloads=20
)

# Then process later
processed_df = processor.process_dataset(
    csv_path=CSV_PATH,
    download_videos=False  # Skip download, use existing videos
)
```

### 6. Analisis Results

```python
if processed_df is not None:
    print(f"Total segments: {len(processed_df)}")
    print(f"Unique videos: {processed_df['video_id'].nunique()}")
    print(f"Label distribution:")
    print(processed_df['label'].value_counts())
    
    # Visualisasi
    from audio_extraction_pipeline import visualize_audio_features
    visualize_audio_features(processed_df)
```

## Contoh Penggunaan Step-by-Step

### Test dengan Single Video

```python
# Test dengan satu video
video_path = "/content/videos/sample_video.mp4"
video_id = "sample_001"
emotion_label = "Joy"

segments = processor.process_single_video(
    video_path, video_id, emotion_label, max_segments=5
)

if segments:
    print(f"Processed {len(segments)} segments")
    print(f"Feature vector length: {len(segments[0]['audio_features'])}")
```

### Batch Processing Dataset

```python
# Format CSV yang diharapkan:
# id,video,emotion
# 001,video_001.mp4,Joy
# 002,video_002.mp4,Sad
# ...

processed_df = processor.process_dataset(CSV_PATH)

# Save additional analysis
from audio_extraction_pipeline import save_feature_summary
save_feature_summary(processed_df, '/content/feature_summary.csv')
```

## Kustomisasi

### 1. Mengubah Parameter Ekstraksi Frame

```python
# Ubah FPS ekstraksi (default: 2 fps)
frame_detector = VideoFrameDetector(fps_extract=1)  # 1 frame per second
processor.frame_detector = frame_detector
```

### 2. Mengubah Parameter Audio Features

```python
# Ubah jumlah MFCC coefficients
feature_extractor = AudioFeatureExtractor(
    sample_rate=22050,
    n_mfcc=20,  # Default: 13
    n_chroma=24  # Default: 12
)
processor.feature_extractor = feature_extractor
```

### 3. Mengubah Durasi Segmen Audio

Modifikasi di method `process_single_video`:

```python
# Di line sekitar 580 dalam DatasetProcessor.process_single_video
segment_duration = 3.0  # Default: 2.0 seconds
start_time = max(0, timestamp - 1.5)  # Default: timestamp - 1.0
```

## Pipeline Architecture

```
Video Input
    ↓
[Frame Extraction] → Deteksi wajah dengan Haar Cascade (2 fps)
    ↓
[Audio Extraction] → Extract full audio menggunakan ffmpeg
    ↓
[Segmentation] → Audio segmen per frame timestamp (±1 detik)
    ↓
[Feature Extraction] → MFCC, Chroma, Spectral Contrast, ZCR
    ↓
[Statistical Aggregation] → Mean, Std, Skewness per feature
    ↓
[Output] → CSV dengan 99 fitur audio per segmen
```

## Pendekatan Multiple Instance Learning (MIL)

Pipeline ini mengimplementasikan pendekatan MIL untuk mengatasi tantangan:
- **Problem**: Label emosi diberikan per video, tapi analisis dilakukan per segmen
- **Solution**: Treat label video sebagai weak supervision
- **Implementation**: 
  - Satu video = satu "bag" berisi banyak segmen
  - Model nantinya belajar bahwa "setidaknya sebagian segmen" mewakili label video
  - Agregasi prediksi segmen dengan voting untuk output final

## Requirements

- Python 3.7+
- librosa >= 0.8.0
- opencv-python >= 4.0.0
- pandas >= 1.0.0
- numpy >= 1.18.0
- scipy >= 1.4.0
- matplotlib >= 3.0.0
- seaborn >= 0.10.0
- tqdm >= 4.50.0
- ffmpeg (system dependency)

## Troubleshooting

### 1. Error "No module named 'librosa'"
```bash
!pip install librosa
```

### 2. Error "ffmpeg not found" 
```bash
!apt update && apt install -y ffmpeg
```

### 3. Error "No faces detected"
- Pastikan video memiliki wajah yang terlihat jelas
- Coba adjust parameter deteksi di `VideoFrameDetector.detect_faces_in_frame()`

### 4. Memory Error saat processing
- Kurangi `max_videos` dan `max_segments_per_video`
- Process dataset dalam batch kecil

### 5. Audio extraction gagal
- Pastikan format video supported (mp4, avi, mov, etc.)
- Check codec video tidak corrupt

## Kontribusi

Pipeline ini dirancang khusus untuk kebutuhan Multimodal Emotion Recognition dengan pendekatan MIL. Untuk improvement atau bug report, silakan buat issue atau pull request.

## License

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan penelitian Anda.