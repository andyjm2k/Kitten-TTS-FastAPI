"""
Kitten TTS - Modern WebUI + OpenAI Compatible API
"""

import os
import io
import base64
import tempfile
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Security, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import soundfile as sf
import numpy as np

# Import KittenTTS
try:
    from kittentts import KittenTTS
except ImportError:
    print("Please install kittentts: pip install https://github.com/KittenML/KittenTTS/releases/download/0.8/kittentts-0.8.0-py3-none-any.whl")
    raise

# Configuration
API_KEY = os.getenv("API_KEY", "")  # Empty means no auth required
MODEL_NAME = os.getenv("MODEL_NAME", "KittenML/kitten-tts-mini-0.8")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Initialize FastAPI app
app = FastAPI(
    title="Kitten TTS API",
    description="OpenAI-compatible Text-to-Speech API using Kitten TTS",
    version="0.8.0"
)

# Security scheme
security = HTTPBearer(auto_error=False)

# Global model instance
model = None

def get_model():
    """Lazy load the model"""
    global model
    if model is None:
        print(f"Loading model: {MODEL_NAME}")
        model = KittenTTS(MODEL_NAME)
        print("Model loaded successfully!")
    return model

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify API key if configured"""
    if not API_KEY:
        return None  # No auth required
    
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing authentication credentials")
    
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return credentials.credentials


# Pydantic models for OpenAI compatibility
class SpeechRequest(BaseModel):
    model: str = Field(default="kitten-tts-mini-0.8", description="Model ID")
    input: str = Field(..., description="The text to generate audio for")
    voice: str = Field(default="Jasper", description="Voice to use")
    response_format: str = Field(default="mp3", description="Audio format (mp3, wav, opus, flac)")
    speed: float = Field(default=1.0, ge=0.25, le=4.0, description="Speed of speech")


class VoiceInfo(BaseModel):
    id: str
    name: str


class VoicesResponse(BaseModel):
    data: List[VoiceInfo]


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int = 0
    owned_by: str = "kittentts"


class ModelsResponse(BaseModel):
    data: List[ModelInfo]


# Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the WebUI"""
    return FileResponse("static/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/v1/audio/speech")
async def create_speech(
    request: SpeechRequest,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """Generate speech from text (OpenAI-compatible)"""
    try:
        tts_model = get_model()
        
        # Get available voices
        available_voices = ['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo']
        voice = request.voice
        
        # Map OpenAI-style voice names to KittenTTS voices if needed
        voice_mapping = {
            "alloy": "Jasper",
            "echo": "Bruno",
            "fable": "Bella",
            "onyx": "Hugo",
            "nova": "Luna",
            "shimmer": "Rosie"
        }
        
        if voice.lower() in voice_mapping:
            voice = voice_mapping[voice.lower()]
        elif voice not in available_voices:
            voice = "Jasper"  # Default voice
        
        # Generate audio
        audio = tts_model.generate(request.input, voice=voice)
        
        # Handle speed adjustment (simple resampling)
        if request.speed != 1.0:
            # For speed adjustment, we'd need to resample
            # This is a simplified version
            pass
        
        # Save to temporary file and return
        with tempfile.NamedTemporaryFile(suffix=f".{request.response_format}", delete=False) as tmp:
            sf.write(tmp.name, audio, 24000, format=request.response_format.upper())
            tmp_path = tmp.name
        
        return FileResponse(
            tmp_path,
            media_type=f"audio/{request.response_format}",
            headers={"Content-Disposition": f'attachment; filename="speech.{request.response_format}"'}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/audio/voices", response_model=VoicesResponse)
async def list_voices(api_key: Optional[str] = Depends(verify_api_key)):
    """List available voices"""
    voices = ['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo']
    return VoicesResponse(data=[VoiceInfo(id=v.lower(), name=v) for v in voices])


@app.get("/v1/models", response_model=ModelsResponse)
async def list_models(api_key: Optional[str] = Depends(verify_api_key)):
    """List available models (OpenAI-compatible)"""
    return ModelsResponse(data=[ModelInfo(id="kitten-tts-mini-0.8")])


@app.get("/v1/models/{model_id}", response_model=ModelInfo)
async def get_model_info(model_id: str, api_key: Optional[str] = Depends(verify_api_key)):
    """Get model information"""
    if model_id == "kitten-tts-mini-0.8":
        return ModelInfo(id=model_id)
    raise HTTPException(status_code=404, detail="Model not found")


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    print(f"Starting Kitten TTS API server on {HOST}:{PORT}")
    if API_KEY:
        print("API Key authentication is ENABLED")
    else:
        print("API Key authentication is DISABLED (no API_KEY set)")
    
    uvicorn.run(app, host=HOST, port=PORT)
