from pydantic import BaseModel
from typing import Optional

class ConversionRequest(BaseModel):
    target_voice_id: Optional[str] = None
    
class ConversionResponse(BaseModel):
    success: bool
    output_path: Optional[str] = None
    duration: Optional[float] = None
    chunks_processed: Optional[int] = None
    error: Optional[str] = None

class VoiceInfo(BaseModel):
    id: str
    display_name: str
    gender: Optional[str] = None
    age_range: Optional[str] = None
    accent: Optional[str] = None
    created_at: str

class AddVoiceRequest(BaseModel):
    voice_id: str
    display_name: str
    gender: Optional[str] = None
    age_range: Optional[str] = None
    accent: Optional[str] = None
