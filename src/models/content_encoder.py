import torch
import torch.nn as nn
import librosa
import numpy as np
from transformers import Wav2Vec2Model, Wav2Vec2Processor

from ..core.config import Config
from ..core.exceptions import ModelLoadingError

class ContentEncoder:
    def __init__(self, config: Config):
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.processor = None
        self.load_model()
    
    def load_model(self):
        """Load content encoder model"""
        try:
            model_name = "facebook/wav2vec2-base-960h"
            self.processor = Wav2Vec2Processor.from_pretrained(model_name)
            self.model = Wav2Vec2Model.from_pretrained(model_name).to(self.device)
            self.model.eval()
        except Exception as e:
            raise ModelLoadingError(f"Failed to load content encoder: {e}")
    
    def extract_content_features(self, audio: np.ndarray) -> torch.Tensor:
        """Extract content features from audio"""
        try:
            # Preprocess audio
            inputs = self.processor(
                audio, 
                sampling_rate=self.config.system.models.sample_rate, 
                return_tensors="pt"
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                content_features = outputs.last_hidden_state
            
            return content_features.squeeze(0)  # Remove batch dimension
        except Exception as e:
            raise ModelLoadingError(f"Failed to extract content features: {e}")
