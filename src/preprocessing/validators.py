import librosa
import numpy as np
from typing import Tuple, Dict

from ..core.config import Config
from ..core.exceptions import ValidationError

class AudioValidator:
    def __init__(self, config: Config):
        self.config = config
        self.min_duration = config.system.processing.min_target_duration
        self.max_duration = config.system.processing.max_audio_length
        self.noise_threshold = config.system.processing.noise_threshold
    
    def validate_audio_file(self, audio_path: str) -> Dict[str, any]:
        """Validate audio file quality and properties"""
        try:
            audio, sr = librosa.load(audio_path, sr=None)
            duration = len(audio) / sr
            
            validation_result = {
                'valid': True,
                'duration': duration,
                'sample_rate': sr,
                'errors': []
            }
            
            # Duration check
            if duration < self.min_duration:
                validation_result['valid'] = False
                validation_result['errors'].append(f"Audio too short: {duration:.1f}s < {self.min_duration}s")
            
            if duration > self.max_duration:
                validation_result['valid'] = False
                validation_result['errors'].append(f"Audio too long: {duration:.1f}s > {self.max_duration}s")
            
            # Quality checks
            snr = self._calculate_snr(audio)
            if snr < self.noise_threshold:
                validation_result['valid'] = False
                validation_result['errors'].append(f"Audio quality too low: SNR {snr:.1f}dB")
            
            validation_result['snr'] = snr
            return validation_result
            
        except Exception as e:
            raise ValidationError(f"Audio validation failed: {e}")
    
    def _calculate_snr(self, audio: np.ndarray) -> float:
        """Calculate Signal-to-Noise Ratio"""
        # Simple SNR estimation
        signal_power = np.mean(audio ** 2)
        noise_estimate = np.std(audio[:int(0.1 * len(audio))])  # First 10% as noise estimate
        noise_power = noise_estimate ** 2
        
        if noise_power == 0:
            return float('inf')
        
        snr_linear = signal_power / noise_power
        snr_db = 10 * np.log10(snr_linear + 1e-10)
        return snr_db
