import torch
import torch.nn as nn
import numpy as np
from resemblyzer import VoiceEncoder
from typing import Optional

from ..core.config import Config
from ..core.exceptions import ModelLoadingError

class SpeakerEncoder:
    def __init__(self, config: Config):
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.encoder = None
        self.load_model()
    
    def load_model(self):
        """Load pre-trained speaker encoder"""
        try:
            self.encoder = VoiceEncoder(device=str(self.device))
        except Exception as e:
            raise ModelLoadingError(f"Failed to load speaker encoder: {e}")
    
    def extract_embedding(self, audio: np.ndarray) -> np.ndarray:
        """Extract speaker embedding from audio"""
        try:
            # Resemblyzer expects audio at 16kHz
            if len(audio.shape) > 1:
                audio = audio.squeeze()
            
            embedding = self.encoder.embed_utterance(audio)
            return embedding
        except Exception as e:
            raise ModelLoadingError(f"Failed to extract speaker embedding: {e}")
    
    def extract_embeddings_from_chunks(self, audio_chunks: list) -> np.ndarray:
        """Extract embeddings from multiple chunks and average"""
        embeddings = []
        for chunk in audio_chunks:
            embedding = self.extract_embedding(chunk)
            embeddings.append(embedding)
        
        # Average embeddings
        averaged_embedding = np.mean(embeddings, axis=0)
        return averaged_embedding
