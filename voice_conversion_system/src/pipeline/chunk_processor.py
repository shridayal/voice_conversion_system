import numpy as np
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import torch

from ..core.config import Config
from ..core.logger import get_logger

logger = get_logger(__name__)

class ChunkProcessor:
    def __init__(self, config: Config, max_workers: int = 4):
        self.config = config
        self.max_workers = max_workers
        
    def process_chunks_parallel(
        self, 
        chunks: List[np.ndarray], 
        target_embedding: np.ndarray,
        conversion_func
    ) -> List[np.ndarray]:
        """Process audio chunks in parallel"""
        
        converted_chunks = [None] * len(chunks)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_index = {
                executor.submit(conversion_func, chunk, target_embedding): i 
                for i, chunk in enumerate(chunks)
            }
            
            # Collect results
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    converted_chunks[index] = future.result()
                    logger.info(f"Completed chunk {index + 1}/{len(chunks)}")
                except Exception as e:
                    logger.error(f"Chunk {index} processing failed: {e}")
                    # Use original chunk as fallback
                    converted_chunks[index] = chunks[index]
        
        return converted_chunks
    
    def combine_chunks_advanced(
        self, 
        chunks: List[np.ndarray], 
        overlap_samples: int
    ) -> np.ndarray:
        """Advanced chunk combination with cross-fading"""
        if len(chunks) == 1:
            return chunks[0]
        
        result = chunks[0].copy()
        
        for i, chunk in enumerate(chunks[1:], 1):
            if len(result) >= overlap_samples and len(chunk) >= overlap_samples:
                # Cross-fade overlapping regions
                fade_out = np.cos(np.linspace(0, np.pi/2, overlap_samples)) ** 2
                fade_in = np.sin(np.linspace(0, np.pi/2, overlap_samples)) ** 2
                
                # Apply fades
                overlap_region = (result[-overlap_samples:] * fade_out + 
                                chunk[:overlap_samples] * fade_in)
                
                # Combine
                result[-overlap_samples:] = overlap_region
                result = np.concatenate([result, chunk[overlap_samples:]])
            else:
                # Simple concatenation if chunks are too short for overlap
                result = np.concatenate([result, chunk])
        
        return result
