from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import tempfile
import os
from pathlib import Path

from ..pipeline.conversion_pipeline import VoiceConversionPipeline
from ..storage.voice_library import VoiceLibrary
from ..core.config import Config
from .models import ConversionRequest, ConversionResponse

app = FastAPI(title="Voice Conversion System", version="1.0.0")

# Initialize components
config = Config()
pipeline = VoiceConversionPipeline()
voice_library = VoiceLibrary(config)

@app.post("/convert", response_model=ConversionResponse)
async def convert_voice(
    source_audio: UploadFile = File(...),
    target_voice_id: str = None,
    target_audio: UploadFile = File(None)
):
    """Convert voice using either library voice or uploaded target"""
    
    if not target_voice_id and not target_audio:
        raise HTTPException(400, "Either target_voice_id or target_audio must be provided")
    
    # Save uploaded source audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_source:
        temp_source.write(await source_audio.read())
        source_path = temp_source.name
    
    try:
        target_path = None
        if target_audio:
            # Save uploaded target audio temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_target:
                temp_target.write(await target_audio.read())
