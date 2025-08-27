#!/usr/bin/env python3
"""
Video Downloader untuk Multimodal Emotion Recognition Pipeline

Module untuk download video dari berbagai sumber:
- Instagram Reels
- Google Drive 
- YouTube
- Direct URL links
- Dan lainnya

Author: Assistant
Created for: Google Colab Environment
"""

import os
import re
import requests
import pandas as pd
from urllib.parse import urlparse, parse_qs
from tqdm import tqdm
import time
import json
import subprocess
from pathlib import Path

class VideoDownloader:
    """
    Class untuk download video dari berbagai sumber
    """
    
    def __init__(self, download_dir="videos", max_retries=3, delay_between_downloads=1):
        self.download_dir = download_dir
        self.max_retries = max_retries
        self.delay_between_downloads = delay_between_downloads
        
        # Create download directory
        os.makedirs(download_dir, exist_ok=True)
        
        # Statistics
        self.download_stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
        
        print(f"VideoDownloader initialized with directory: {download_dir}")
    
    def _get_file_extension_from_url(self, url):
        """Deteksi extension file dari URL"""
        try:
            # Parse URL
            parsed = urlparse(url)
            path = parsed.path.lower()
            
            # Check common video extensions
            video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv']
            for ext in video_extensions:
                if path.endswith(ext):
                    return ext
            
            # Default to .mp4 if no extension found
            return '.mp4'
        except:
            return '.mp4'
    
    def _sanitize_filename(self, filename):
        """Sanitize filename untuk sistem file"""
        # Remove/replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\s+', '_', filename)  # Replace spaces with underscore
        filename = filename[:100]  # Limit length
        return filename
    
    def _download_direct_url(self, url, output_path):
        """Download video dari direct URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(output_path, 'wb') as f:
                if total_size > 0:
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                else:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            
            return True
        except Exception as e:
            print(f"Error downloading direct URL: {e}")
            return False
    
    def _download_google_drive(self, url, output_path):
        """Download video dari Google Drive"""
        try:
            # Extract file ID from Google Drive URL
            file_id = None
            
            # Pattern untuk berbagai format Google Drive URL
            patterns = [
                r'/file/d/([a-zA-Z0-9-_]+)',
                r'id=([a-zA-Z0-9-_]+)',
                r'/open\?id=([a-zA-Z0-9-_]+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    file_id = match.group(1)
                    break
            
            if not file_id:
                print(f"Could not extract file ID from Google Drive URL: {url}")
                return False
            
            # Use gdown if available, otherwise fallback to requests
            try:
                import gdown
                gdown.download(f"https://drive.google.com/uc?id={file_id}", output_path, quiet=False)
                return True
            except ImportError:
                print("gdown not available, trying alternative method...")
                
                # Alternative method using requests
                download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                
                session = requests.Session()
                response = session.get(download_url, stream=True)
                
                # Handle large file confirmation
                for key, value in response.cookies.items():
                    if key.startswith('download_warning'):
                        download_url = f"https://drive.google.com/uc?export=download&confirm={value}&id={file_id}"
                        response = session.get(download_url, stream=True)
                        break
                
                # Save file
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                return True
                
        except Exception as e:
            print(f"Error downloading from Google Drive: {e}")
            return False
    
    def _download_instagram_reel(self, url, output_path):
        """Download Instagram Reel"""
        try:
            # Try using yt-dlp (recommended) or youtube-dl
            try:
                # Try yt-dlp first
                cmd = [
                    'yt-dlp',
                    '--format', 'best[ext=mp4]',
                    '--output', output_path,
                    '--no-warnings',
                    url
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    return True
                else:
                    print(f"yt-dlp failed: {result.stderr}")
            except FileNotFoundError:
                print("yt-dlp not found, trying youtube-dl...")
                
                # Fallback to youtube-dl
                cmd = [
                    'youtube-dl',
                    '--format', 'best[ext=mp4]',
                    '--output', output_path,
                    '--no-warnings',
                    url
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    return True
                else:
                    print(f"youtube-dl failed: {result.stderr}")
            
            # If both fail, try alternative approach
            print("Trying alternative Instagram download method...")
            return self._download_instagram_alternative(url, output_path)
            
        except Exception as e:
            print(f"Error downloading Instagram reel: {e}")
            return False
    
    def _download_instagram_alternative(self, url, output_path):
        """Alternative method untuk download Instagram"""
        try:
            # This is a simplified approach - in practice, you might need
            # to use specialized Instagram downloaders or APIs
            
            # Try to extract shortcode from URL
            shortcode_match = re.search(r'/reel/([^/?]+)', url)
            if not shortcode_match:
                shortcode_match = re.search(r'/p/([^/?]+)', url)
            
            if shortcode_match:
                shortcode = shortcode_match.group(1)
                print(f"Extracted shortcode: {shortcode}")
                
                # Note: This is a placeholder - actual implementation would need
                # to use Instagram's API or specialized tools
                print("Alternative Instagram download not fully implemented.")
                print("Please use yt-dlp or youtube-dl for Instagram downloads.")
                return False
            else:
                print("Could not extract shortcode from Instagram URL")
                return False
                
        except Exception as e:
            print(f"Error in alternative Instagram download: {e}")
            return False
    
    def _download_youtube(self, url, output_path):
        """Download video dari YouTube"""
        try:
            # Try using yt-dlp first, then youtube-dl
            try:
                cmd = [
                    'yt-dlp',
                    '--format', 'best[ext=mp4]',
                    '--output', output_path,
                    '--no-warnings',
                    url
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    return True
                else:
                    print(f"yt-dlp failed: {result.stderr}")
            except FileNotFoundError:
                print("yt-dlp not found, trying youtube-dl...")
                
                cmd = [
                    'youtube-dl',
                    '--format', 'best[ext=mp4]',
                    '--output', output_path,
                    '--no-warnings',
                    url
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    return True
                else:
                    print(f"youtube-dl failed: {result.stderr}")
            
            return False
            
        except Exception as e:
            print(f"Error downloading YouTube video: {e}")
            return False
    
    def detect_video_source(self, url):
        """Deteksi sumber video dari URL"""
        url_lower = url.lower()
        
        if 'instagram.com' in url_lower:
            return 'instagram'
        elif 'drive.google.com' in url_lower:
            return 'google_drive'
        elif 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'youtube'
        elif any(ext in url_lower for ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']):
            return 'direct_url'
        else:
            return 'unknown'
    
    def download_single_video(self, url, video_id, output_filename=None):
        """
        Download satu video dari URL
        
        Args:
            url (str): URL video
            video_id (str): ID unik untuk video
            output_filename (str): Nama file output (optional)
        
        Returns:
            str: Path ke file yang didownload, atau None jika gagal
        """
        if output_filename is None:
            extension = self._get_file_extension_from_url(url)
            output_filename = f"{self._sanitize_filename(video_id)}{extension}"
        
        output_path = os.path.join(self.download_dir, output_filename)
        
        # Skip if file already exists
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"File already exists: {output_filename}")
            self.download_stats['skipped'] += 1
            return output_path
        
        # Detect video source
        source = self.detect_video_source(url)
        print(f"Downloading {video_id} from {source}: {url}")
        
        # Try download with retries
        success = False
        for attempt in range(self.max_retries):
            try:
                if source == 'instagram':
                    success = self._download_instagram_reel(url, output_path)
                elif source == 'google_drive':
                    success = self._download_google_drive(url, output_path)
                elif source == 'youtube':
                    success = self._download_youtube(url, output_path)
                elif source == 'direct_url':
                    success = self._download_direct_url(url, output_path)
                else:
                    print(f"Unknown source type: {source}")
                    # Try as direct URL as fallback
                    success = self._download_direct_url(url, output_path)
                
                if success:
                    break
                else:
                    print(f"Attempt {attempt + 1} failed for {video_id}")
                    if attempt < self.max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        
            except Exception as e:
                print(f"Error on attempt {attempt + 1} for {video_id}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
        
        # Check if download was successful
        if success and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"✓ Successfully downloaded: {output_filename}")
            self.download_stats['success'] += 1
            
            # Add delay between downloads to be respectful
            time.sleep(self.delay_between_downloads)
            
            return output_path
        else:
            print(f"✗ Failed to download: {video_id}")
            self.download_stats['failed'] += 1
            
            # Clean up failed download
            if os.path.exists(output_path):
                os.remove(output_path)
            
            return None
    
    def download_from_csv(self, csv_path, video_col='video', id_col='id', max_downloads=None):
        """
        Download videos dari CSV dataset
        
        Args:
            csv_path (str): Path ke file CSV
            video_col (str): Nama kolom yang berisi URL video
            id_col (str): Nama kolom yang berisi ID video
            max_downloads (int): Maksimal jumlah download (None = unlimited)
        
        Returns:
            pd.DataFrame: Updated dataframe dengan kolom 'local_path'
        """
        try:
            # Load CSV
            df = pd.read_csv(csv_path)
            print(f"Loaded dataset with {len(df)} entries")
            print(f"Columns: {list(df.columns)}")
            
            if video_col not in df.columns or id_col not in df.columns:
                print(f"Required columns not found. Expected: {video_col}, {id_col}")
                return None
            
            # Add local_path column
            df['local_path'] = None
            df['download_status'] = 'pending'
            
            # Reset stats
            self.download_stats = {'total': 0, 'success': 0, 'failed': 0, 'skipped': 0}
            
            # Process each row
            total_to_download = min(len(df), max_downloads) if max_downloads else len(df)
            
            with tqdm(total=total_to_download, desc="Downloading videos") as pbar:
                for idx, row in df.iterrows():
                    if max_downloads and idx >= max_downloads:
                        break
                    
                    video_url = row[video_col]
                    video_id = str(row[id_col])
                    
                    self.download_stats['total'] += 1
                    
                    # Skip empty URLs
                    if pd.isna(video_url) or str(video_url).strip() == '':
                        print(f"Skipping empty URL for ID: {video_id}")
                        df.at[idx, 'download_status'] = 'empty_url'
                        pbar.update(1)
                        continue
                    
                    # Download video
                    local_path = self.download_single_video(video_url, video_id)
                    
                    if local_path:
                        df.at[idx, 'local_path'] = local_path
                        df.at[idx, 'download_status'] = 'success'
                    else:
                        df.at[idx, 'download_status'] = 'failed'
                    
                    pbar.update(1)
            
            # Save updated CSV
            output_csv_path = csv_path.replace('.csv', '_with_downloads.csv')
            df.to_csv(output_csv_path, index=False)
            print(f"\nUpdated CSV saved to: {output_csv_path}")
            
            # Print statistics
            self.print_download_stats()
            
            return df
            
        except Exception as e:
            print(f"Error processing CSV: {e}")
            return None
    
    def print_download_stats(self):
        """Print download statistics"""
        stats = self.download_stats
        total = stats['total']
        
        print(f"\n=== Download Statistics ===")
        print(f"Total videos: {total}")
        print(f"Successfully downloaded: {stats['success']} ({stats['success']/total*100:.1f}%)")
        print(f"Already existed (skipped): {stats['skipped']} ({stats['skipped']/total*100:.1f}%)")
        print(f"Failed: {stats['failed']} ({stats['failed']/total*100:.1f}%)")
        print(f"Success rate: {(stats['success'] + stats['skipped'])/total*100:.1f}%")
    
    def get_failed_downloads(self, df):
        """Get list of failed downloads for retry"""
        if df is None:
            return None
        
        failed_df = df[df['download_status'] == 'failed'].copy()
        return failed_df
    
    def retry_failed_downloads(self, df, max_retries=1):
        """Retry failed downloads"""
        failed_df = self.get_failed_downloads(df)
        
        if failed_df is None or len(failed_df) == 0:
            print("No failed downloads to retry")
            return df
        
        print(f"Retrying {len(failed_df)} failed downloads...")
        
        for idx, row in failed_df.iterrows():
            video_url = row['video']
            video_id = str(row['id'])
            
            print(f"Retrying: {video_id}")
            local_path = self.download_single_video(video_url, video_id)
            
            if local_path:
                df.at[idx, 'local_path'] = local_path
                df.at[idx, 'download_status'] = 'success'
                self.download_stats['success'] += 1
                self.download_stats['failed'] -= 1
        
        return df

def install_download_dependencies():
    """Install dependencies untuk video download"""
    print("Installing video download dependencies...")
    
    try:
        # Install yt-dlp (recommended)
        subprocess.check_call(['pip', 'install', 'yt-dlp'])
        print("✓ yt-dlp installed")
    except:
        print("✗ Failed to install yt-dlp")
    
    try:
        # Install gdown untuk Google Drive
        subprocess.check_call(['pip', 'install', 'gdown'])
        print("✓ gdown installed")
    except:
        print("✗ Failed to install gdown")
    
    try:
        # Install youtube-dl sebagai fallback
        subprocess.check_call(['pip', 'install', 'youtube-dl'])
        print("✓ youtube-dl installed")
    except:
        print("✗ Failed to install youtube-dl")
    
    print("Dependencies installation completed!")

# Example usage
def main():
    """Demo function"""
    print("=== Video Downloader Demo ===")
    
    # Initialize downloader
    downloader = VideoDownloader(download_dir="downloaded_videos")
    
    # Example: Download from CSV
    csv_path = "datatrain.csv"
    
    if os.path.exists(csv_path):
        print(f"Processing CSV: {csv_path}")
        df = downloader.download_from_csv(
            csv_path, 
            video_col='video', 
            id_col='id',
            max_downloads=5  # Limit untuk demo
        )
        
        if df is not None:
            print("\nDownload completed!")
            print(f"Successful downloads: {len(df[df['download_status'] == 'success'])}")
            
            # Show successful downloads
            successful = df[df['download_status'] == 'success']
            if len(successful) > 0:
                print("\nSuccessfully downloaded files:")
                for _, row in successful.iterrows():
                    print(f"  {row['id']}: {row['local_path']}")
    else:
        print(f"CSV file not found: {csv_path}")
        print("Please ensure your CSV file exists with 'id' and 'video' columns")

if __name__ == "__main__":
    main()