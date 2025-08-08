import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

@dataclass
class ModelConfig:
    speaker_encoder_model: str
    content_encoder_model: str
    voice_converter_model: str
    vocoder_model: str
    sample_rate: int
    hop_length: int
    win_length: int
    n_mels: int
    
@dataclass
class ProcessingConfig:
    chunk_duration: float
    overlap_duration: float
    max_audio_length: int
    min_target_duration: float
    noise_threshold: float

@dataclass
class SystemConfig:
    models: ModelConfig
    processing: ProcessingConfig
    cache_dir: str
    temp_dir: str
    voice_library_dir: str
    
class Config:
    def __init__(self, config_path: str = "config/system_config.yaml"):
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        self.system = SystemConfig(**config_data)
        self._setup_directories()
    
    def _setup_directories(self):
        Path(self.system.cache_dir).mkdir(parents=True, exist_ok=True)
        Path(self.system.temp_dir).mkdir(parents=True, exist_ok=True)
        Path(self.system.voice_library_dir).mkdir(parents=True, exist_ok=True)
