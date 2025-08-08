import torch
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any
import soundfile as sf

from ..core.config import Config
from ..core.logger import get_logger
from ..preprocessing.audio_processor import AudioProcessor
from ..preprocessing.validators import AudioValidator
from ..models.speaker_encoder import SpeakerEncoder
from ..models.content_encoder import ContentEncoder
from ..storage.voice_library import VoiceLibrary
from ..storage.cache_manager import CacheManager

logger = get_logger(__name__)

class VoiceConversionPipeline:
    def __init__(self, config_path: str = "config/system_config.yaml"):
        self.config = Config(config_path)
        self.audio_processor = AudioProcessor(self.config)
        self.validator = AudioValidator(self.config)
        self.speaker_encoder = SpeakerEncoder(self.config)
        self.content_encoder = ContentEncoder(self.config)
        self.voice_library = VoiceLibrary(self.config)
        self.cache_manager = CacheManager(self.config)
    
    def convert_voice(
        self, 
        source_audio_path: str, 
        target_voice_id: Optional[str] = None,
        target_audio_path: Optional[str] = None,
        output_path: str = "output.wav"
    ) -> Dict[str, Any]:
        """
        Main voice conversion method
        
        Args:
            source_audio_path: Path to source audio
            target_voice_id: ID from voice library (optional)
            target_audio_path: Path to target voice sample (optional) 
            output_path: Output file path
        """
        try:
            logger.info("Starting voice conversion process")
            
            # Validate inputs
            self._validate_inputs(source_audio_path, target_voice_id, target_audio_path)
            
            # Process source audio
            logger.info("Processing source audio")
            source_audio = self.audio_processor.preprocess_audio(source_audio_path)
            
            # Get target speaker embedding
            logger.info("Extracting target speaker embedding")
            target_embedding = self._get_target_embedding(target_voice_id, target_audio_path)
            
            # Process audio in chunks for longer files
            chunks = self.audio_processor.chunk_audio(
                source_audio,
                self.config.system.processing.chunk_duration,
                self.config.system.processing.overlap_duration
            )
            
            logger.info(f"Processing {len(chunks)} audio chunks")
            converted_chunks = []
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Processing chunk {i+1}/{len(chunks)}")
                converted_chunk = self._convert_chunk(chunk, target_embedding)
                converted_chunks.append(converted_chunk)
            
            # Combine chunks
            logger.info("Combining converted chunks")
            final_audio = self._combine_chunks(converted_chunks)
            
            # Save output
            sf.write(output_path, final_audio, self.config.system.models.sample_rate)
            
            logger.info(f"Voice conversion completed. Output saved to: {output_path}")
            
            return {
                'success': True,
                'output_path': output_path,
                'duration': len(final_audio) / self.config.system.models.sample_rate,
                'chunks_processed': len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Voice conversion failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _validate_inputs(self, source_path, target_voice_id, target_audio_path):
        """Validate input parameters"""
        if not Path(source_path).exists():
            raise FileNotFoundError(f"Source audio not found: {source_path}")
        
        if target_voice_id is None and target_audio_path is None:
            raise ValueError("Either target_voice_id or target_audio_path must be provided")
        
        if target_audio_path and not Path(target_audio_path).exists():
            raise FileNotFoundError(f"Target audio not found: {target_audio_path}")
    
    def _get_target_embedding(self, voice_id: Optional[str], audio_path: Optional[str]) -> np.ndarray:
        """Get target speaker embedding from library or uploaded file"""
        if voice_id:
            # Get from voice library
            return self.voice_library.get_voice_embedding(voice_id)
        else:
            # Process uploaded target voice
            validation_result = self.validator.validate_audio_file(audio_path)
            if not validation_result['valid']:
                raise ValueError(f"Invalid target audio: {validation_result['errors']}")
            
            target_audio = self.audio_processor.preprocess_audio(audio_path)
            return self.speaker_encoder.extract_embedding(target_audio)
    
    def _convert_chunk(self, audio_chunk: np.ndarray, target_embedding: np.ndarray) -> np.ndarray:
        """Convert a single audio chunk"""
        # Extract content features
        content_features = self.content_encoder.extract_content_features(audio_chunk)
        
        # This is where you'd integrate your actual voice conversion model
        # For now, returning the original chunk as placeholder
        # In real implementation, you'd use AutoVC, VQ-VAE, or GAN-based model
        
        # Placeholder conversion logic
        converted_chunk = self._apply_voice_conversion(
            audio_chunk, content_features, target_embedding
        )
        
        return converted_chunk
    
    def _apply_voice_conversion(
        self, 
        audio: np.ndarray, 
        content: torch.Tensor, 
        speaker_embedding: np.ndarray
    ) -> np.ndarray:
        """
        Placeholder for actual voice conversion model
        Replace with your chosen model (AutoVC, VQ-VAE, etc.)
        """
        # This is where the magic happens with your chosen model
        # For MVP, you could start with a simple spectral manipulation approach
        
        # Placeholder: return original audio (replace with actual conversion)
        logger.warning("Using placeholder conversion - implement actual model here")
        return audio
    
    def _combine_chunks(self, chunks: list) -> np.ndarray:
        """Combine overlapping chunks using overlap-add method"""
        if len(chunks) == 1:
            return chunks[0]
        
        overlap_samples = int(
            self.config.system.processing.overlap_duration * 
            self.config.system.models.sample_rate
        )
        
        # Simple concatenation with fade in/out for overlap
        result = chunks[0]
        
        for chunk in chunks[1:]:
            # Apply fade in/out for smoother transitions
            if len(result) >= overlap_samples:
                fade_out = np.linspace(1, 0, overlap_samples)
                fade_in = np.linspace(0, 1, overlap_samples)
                
                result[-overlap_samples:] *= fade_out
                chunk[:overlap_samples] *= fade_in
                
                result[-overlap_samples:] += chunk[:overlap_samples]
                result = np.concatenate([result, chunk[overlap_samples:]])
            else:
                result = np.concatenate([result, chunk])
        
        return result
