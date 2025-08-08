import librosa
import numpy as np
import torch
import torchaudio
from typing import Tuple, Optional
from pathlib import Path
import noisereduce as nr

from ..core.config import Config
from ..core.exceptions import AudioProcessingError

class AudioProcessor:
    def __init__(self, config: Config):
        self.config = config
        self.sample_rate = config.system.models.sample_rate
        
    def load_audio(self, audio_path: str) -> np.ndarray:
        """Load and preprocess audio file"""
        try:
            audio, sr = librosa.load(audio_path, sr=self.sample_rate, mono=True)
            return audio
        except Exception as e:
            raise AudioProcessingError(f"Failed to load audio: {e}")
    
    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """Normalize audio amplitude"""
        audio = audio / np.max(np.abs(audio) + 1e-9)
        return audio
    
    def reduce_noise(self, audio: np.ndarray) -> np.ndarray:
        """Apply noise reduction"""
        try:
            reduced_noise = nr.reduce_noise(y=audio, sr=self.sample_rate)
            return reduced_noise
        except Exception as e:
            print(f"Noise reduction warning: {e}")
            return audio
    
    def trim_silence(self, audio: np.ndarray, threshold: float = 0.01) -> np.ndarray:
        """Remove silence from beginning and end"""
        trimmed, _ = librosa.effects.trim(audio, top_db=20)
        return trimmed
    
    def preprocess_audio(self, audio_path: str) -> np.ndarray:
        """Complete preprocessing pipeline"""
        audio = self.load_audio(audio_path)
        audio = self.normalize_audio(audio)
        audio = self.reduce_noise(audio)
        audio = self.trim_silence(audio)
        return audio
    
    def chunk_audio(self, audio: np.ndarray, chunk_duration: float, overlap: float) -> list:
        """Split audio into overlapping chunks"""
        chunk_samples = int(chunk_duration * self.sample_rate)
        overlap_samples = int(overlap * self.sample_rate)
        step = chunk_samples - overlap_samples
        
        chunks = []
        for i in range(0, len(audio) - chunk_samples + 1, step):
            chunk = audio[i:i + chunk_samples]
            chunks.append(chunk)
        
        # Handle remaining audio
        if len(audio) % step != 0:
            chunks.append(audio[-chunk_samples:])
            
        return chunks
