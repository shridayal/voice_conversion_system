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
                                target_path = temp_target.name
        
        # Generate output path
        output_path = tempfile.mktemp(suffix=".wav")
        
        # Perform conversion
        result = pipeline.convert_voice(
            source_audio_path=source_path,
            target_voice_id=target_voice_id,
            target_audio_path=target_path,
            output_path=output_path
        )
        
        if not result['success']:
            raise HTTPException(500, f"Conversion failed: {result['error']}")
        
        return ConversionResponse(
            success=True,
            output_path=output_path,
            duration=result['duration'],
            chunks_processed=result['chunks_processed']
        )
    
    finally:
        # Cleanup temporary files
        if os.path.exists(source_path):
            os.unlink(source_path)
        if target_path and os.path.exists(target_path):
            os.unlink(target_path)

@app.get("/download/{file_path}")
async def download_converted_audio(file_path: str):
    """Download converted audio file"""
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    return FileResponse(
        file_path,
        media_type="audio/wav",
        filename="converted_audio.wav"
    )

@app.get("/voices")
async def list_voices():
    """List available voices in the library"""
    return voice_library.list_voices()

@app.post("/voices")
async def add_voice(
    voice_id: str,
    display_name: str,
    voice_audio: UploadFile = File(...),
    gender: str = None,
    age_range: str = None,
    accent: str = None
):
    """Add a new voice to the library"""
    
    # Save uploaded audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(await voice_audio.read())
        temp_path = temp_file.name
    
    try:
        # Process and extract embedding
        audio = pipeline.audio_processor.preprocess_audio(temp_path)
        embedding = pipeline.speaker_encoder.extract_embedding(audio)
        
        # Add to library
        metadata = {
            'display_name': display_name,
            'gender': gender,
            'age_range': age_range,
            'accent': accent,
            'created_at': str(datetime.now())
        }
        
        voice_library.add_voice(voice_id, embedding, metadata)
        
        return {"message": f"Voice {voice_id} added successfully"}
    
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@app.delete("/voices/{voice_id}")
async def remove_voice(voice_id: str):
    """Remove a voice from the library"""
    voice_library.remove_voice(voice_id)
    return {"message": f"Voice {voice_id} removed successfully"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}
                

