import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np

from ..core.config import Config
from ..core.logger import get_logger

logger = get_logger(__name__)

class VoiceLibrary:
    def __init__(self, config: Config):
        self.config = config
        self.library_path = Path(config.system.voice_library_dir)
        self.metadata_file = self.library_path / "metadata.json"
        self.embeddings_dir = self.library_path / "embeddings"
        
        self._ensure_directories()
        self.metadata = self._load_metadata()
    
    def _ensure_directories(self):
        """Create necessary directories"""
        self.library_path.mkdir(parents=True, exist_ok=True)
        self.embeddings_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_metadata(self) -> Dict:
        """Load voice library metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_metadata(self):
        """Save voice library metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def add_voice(
        self, 
        voice_id: str, 
        embedding: np.ndarray, 
        metadata: Dict
    ):
        """Add a voice to the library"""
        embedding_path = self.embeddings_dir / f"{voice_id}.npy"
        np.save(embedding_path, embedding)
        
        self.metadata[voice_id] = {
            'embedding_path': str(embedding_path),
            **metadata
        }
        
        self._save_metadata()
        logger.info(f"Added voice {voice_id} to library")
    
    def get_voice_embedding(self, voice_id: str) -> np.ndarray:
        """Get voice embedding by ID"""
        if voice_id not in self.metadata:
            raise ValueError(f"Voice ID {voice_id} not found in library")
        
        embedding_path = self.metadata[voice_id]['embedding_path']
        return np.load(embedding_path)
    
    def list_voices(self) -> List[Dict]:
        """List all available voices"""
        voices = []
        for voice_id, data in self.metadata.items():
            voice_info = {
                'id': voice_id,
                **{k: v for k, v in data.items() if k != 'embedding_path'}
            }
            voices.append(voice_info)
        return voices
    
    def remove_voice(self, voice_id: str):
        """Remove a voice from the library"""
        if voice_id in self.metadata:
            embedding_path = Path(self.metadata[voice_id]['embedding_path'])
            if embedding_path.exists():
                embedding_path.unlink()
            
            del self.metadata[voice_id]
            self._save_metadata()
            logger.info(f"Removed voice {voice_id} from library")
