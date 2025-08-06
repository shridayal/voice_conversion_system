class VoiceConversionError(Exception):
    """Base exception for voice conversion system"""
    pass

class AudioProcessingError(VoiceConversionError):
    """Audio processing related errors"""
    pass

class ModelLoadingError(VoiceConversionError):
    """Model loading related errors"""
    pass

class ValidationError(VoiceConversionError):
    """Audio validation related errors"""
    pass
