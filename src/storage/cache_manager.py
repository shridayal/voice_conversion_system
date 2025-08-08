import pickle
import hashlib
from pathlib import Path
from typing import Any, Optional
import numpy as np
from datetime import datetime, timedelta

from ..core.config import Config
from ..core.logger import get_logger

logger = get_logger(__name__)

class CacheManager:
    def __init__(self, config: Config, max_cache_size_mb: int = 500):
        self.config = config
        self.cache_dir = Path(config.system.cache_dir)
        self.max_cache_size = max_cache_size_mb * 1024 * 1024  # Convert to bytes
        self.cache_duration = timedelta(hours=24)  # Cache for 24 hours
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_cache_key(self, data: Any) -> str:
        """Generate cache key from data"""
        if isinstance(data, np.ndarray):
            data_bytes = data.tobytes()
        elif isinstance(data, str):
            data_bytes = data.encode()
        else:
            data_bytes = str(data).encode()
        
        return hashlib.md5(data_bytes).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache"""
        cache_file = self.cache_dir / f"{key}.cache"
        
        if not cache_file.exists():
            return None
        
        # Check if cache is expired
        file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if datetime.now() - file_time > self.cache_duration:
            cache_file.unlink()
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logger.warning(f"Failed to load cache {key}: {e}")
            return None
    
    def set(self, key: str, data: Any):
        """Set item in cache"""
        cache_file = self.cache_dir / f"{key}.cache"
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
            
            # Clean cache if it's getting too large
            self._cleanup_cache()
            
        except Exception as e:
            logger.warning(f"Failed to save cache {key}: {e}")
    
    def cache_speaker_embedding(self, audio_path: str, embedding: np.ndarray):
        """Cache speaker embedding for audio file"""
        key = self._generate_cache_key(audio_path + str(Path(audio_path).stat().st_mtime))
        self.set(f"speaker_emb_{key}", embedding)
    
    def get_cached_speaker_embedding(self, audio_path: str) -> Optional[np.ndarray]:
        """Get cached speaker embedding"""
        key = self._generate_cache_key(audio_path + str(Path(audio_path).stat().st_mtime))
        return self.get(f"speaker_emb_{key}")
    
    def _cleanup_cache(self):
        """Remove old cache files if cache size exceeds limit"""
        cache_files = list(self.cache_dir.glob("*.cache"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        if total_size > self.max_cache_size:
            # Sort by modification time, oldest first
            cache_files.sort(key=lambda x: x.stat().st_mtime)
            
            # Remove oldest files until under limit
            for cache_file in cache_files:
                cache_file.unlink()
                total_size -= cache_file.stat().st_size
                logger.info(f"Removed old cache file: {cache_file.name}")
                
                if total_size <= self.max_cache_size * 0.8:  # Keep 20% buffer
                    break
    
    def clear_cache(self):
        """Clear all cache files"""
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink()
        logger.info("Cache cleared")
