# 🏗️ Kitten TTS Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Applications                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Web UI  │  │  Python  │  │    JS    │  │   cURL   │   │
│  │          │  │  Script  │  │  Client  │  │          │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
              HTTP/REST API
                      │
┌─────────────────────▼──────────────────────────────────────┐
│                   FastAPI Server (app.py)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  API Endpoints                        │  │
│  │  • POST /v1/audio/speech     (OpenAI-compatible)     │  │
│  │  • GET  /v1/audio/voices     (List voices)           │  │
│  │  • GET  /v1/models           (List models)           │  │
│  │  • GET  /health              (Health check)          │  │
│  │  • GET  /                    (WebUI)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               Security Layer (Optional)               │  │
│  │         API Key Authentication (Bearer Token)         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────┬──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   KittenTTS Model Layer                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Voice Selection & Mapping                │  │
│  │  OpenAI Names → KittenTTS Voices                      │  │
│  │  (alloy→Jasper, echo→Bruno, etc.)                     │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Text-to-Speech Generation                  │  │
│  │  • Input: Text + Voice                                │  │
│  │  • Output: Audio Array (numpy)                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────┬──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Audio Processing                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              SoundFile Library                        │  │
│  │  Format Conversion: MP3, WAV, Opus, FLAC             │  │
│  │  Sample Rate: 24kHz                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. **Client Layer**
- **Web UI**: Modern HTML5/CSS3/JavaScript interface
- **Python Client**: requests library
- **JavaScript Client**: Fetch API / Axios
- **Any HTTP Client**: cURL, Postman, etc.

### 2. **API Layer (FastAPI)**
- **Framework**: FastAPI (async, auto-docs)
- **Endpoints**: OpenAI-compatible REST API
- **Security**: Optional Bearer token authentication
- **Validation**: Pydantic models for request/response

### 3. **Model Layer (KittenTTS)**
- **Model**: KittenML/kitten-tts-mini-0.8
- **Size**: ~79MB (80M parameters)
- **Architecture**: StyleTTS 2
- **Voices**: 8 pre-trained voices
- **Hardware**: CPU-only (no GPU required)

### 4. **Audio Layer**
- **Library**: SoundFile (libsndfile binding)
- **Formats**: MP3, WAV, Opus, FLAC
- **Sample Rate**: 24kHz
- **Processing**: NumPy arrays

## Data Flow

### Speech Generation Request

```
1. Client sends POST /v1/audio/speech
   {
     "model": "kitten-tts-mini-0.8",
     "input": "Hello world!",
     "voice": "Jasper",
     "response_format": "mp3"
   }

2. API validates request
   ✓ Check API key (if enabled)
   ✓ Validate parameters
   ✓ Map voice names (OpenAI → KittenTTS)

3. Model generates audio
   ✓ Load model (lazy, first request)
   ✓ Generate audio array
   ✓ Convert to requested format

4. Return audio file
   ✓ Binary response
   ✓ Content-Type: audio/<format>
   ✓ Ready for playback/download
```

## Deployment Architecture

### Docker Deployment

```
┌─────────────────────────────────────────┐
│         Host Machine                    │
│  ┌───────────────────────────────────┐  │
│  │      Docker Container             │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │   Kitten TTS Application    │  │  │
│  │  │   - FastAPI Server          │  │  │
│  │  │   - KittenTTS Model         │  │  │
│  │  │   - Dependencies            │  │  │
│  │  └─────────────────────────────┘  │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │   Volume: HF Cache          │  │  │
│  │  │   (persist model files)     │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
│         Port: 8000                      │
└─────────────────────────────────────────┘
```

### Production Deployment

```
                    ┌─────────────┐
                    │   Users     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Load       │
                    │  Balancer   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌───▼────┐ ┌────▼────┐
       │   nginx     │ │ nginx  │ │  nginx  │
       │  (HTTPS)    │ │(HTTPS) │ │ (HTTPS) │
       └──────┬──────┘ └───┬────┘ └────┬────┘
              │            │            │
       ┌──────▼──────┐ ┌───▼────┐ ┌────▼────┐
       │  Container  │ │Container│ │Container│
       │  Kitten TTS │ │Kitten   │ │Kitten   │
       │             │ │TTS      │ │TTS      │
       └─────────────┘ └─────────┘ └─────────┘
```

## Security Model

### Without API Key (Development)
```
Client → API → Model → Response
(No authentication)
```

### With API Key (Production)
```
Client → [Auth Check] → API → Model → Response
         ↑
    Bearer Token
```

## Configuration Layers

```
┌─────────────────────────────────────┐
│  Environment Variables              │
│  (Highest Priority)                 │
│  - API_KEY                          │
│  - PORT                             │
│  - HOST                             │
│  - MODEL_NAME                       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  .env File                          │
│  (Local Development)                │
│  - API_KEY=...                      │
│  - PORT=8000                        │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  docker-compose.yml                 │
│  (Container Deployment)             │
│  - environment:                     │
│      - API_KEY=...                  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Default Values (app.py)            │
│  (Lowest Priority)                  │
│  - PORT=8000                        │
│  - HOST=0.0.0.0                     │
│  - API_KEY=""                       │
└─────────────────────────────────────┘
```

## File Structure

```
kitten-tts/
├── app.py                      # Main FastAPI application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker build config
├── docker-compose.yml          # Docker Compose (no auth)
├── docker-compose.api-key.yml  # Docker Compose (with auth)
├── .dockerignore              # Docker ignore patterns
├── .env.example               # Environment template
├── start.sh                   # Startup script
│
├── static/
│   └── index.html             # WebUI
│
├── examples/
│   ├── usage_examples.py      # Python examples
│   └── usage_examples.js      # JavaScript examples
│
├── test_api.py                # API test suite
│
└── Documentation/
    ├── README.md              # Full documentation
    ├── QUICKSTART.md          # Quick start guide
    ├── PUBLISHING_GUIDE.md    # Docker publishing guide
    └── ARCHITECTURE.md        # This file
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | REST API framework |
| **TTS Model** | KittenTTS 0.8 | Text-to-speech generation |
| **Audio** | SoundFile | Audio encoding/decoding |
| **Math** | NumPy | Array operations |
| **Server** | Uvicorn | ASGI server |
| **Container** | Docker | Deployment |
| **Frontend** | HTML5/CSS3/JS | Web interface |
| **Security** | HTTPBearer | API key auth |

## Performance Characteristics

### Resource Usage
- **Memory**: ~500MB - 1GB (model + runtime)
- **CPU**: Single-threaded generation
- **Disk**: ~100MB (model cache)
- **Startup**: 5-10 seconds (model load)

### Latency
- **First Request**: 5-10s (model loading)
- **Subsequent**: 1-3s per sentence
- **Factors**: Text length, voice, CPU speed

### Throughput
- **Concurrent Requests**: Limited (single model instance)
- **Recommendation**: Queue or load balance for high traffic

## Scalability Options

### Vertical Scaling
- More CPU cores → Faster generation
- More RAM → Better multitasking

### Horizontal Scaling
```
Load Balancer → Multiple Kitten TTS Instances
```

### Caching Strategy
```
Request → Check Cache → Hit: Return Cached
                    → Miss: Generate + Cache
```

## Monitoring & Observability

### Health Checks
- `GET /health` - Basic health status
- Docker HEALTHCHECK - Container health

### Logging
- FastAPI access logs
- Application logs (model load, errors)

### Metrics (Future Enhancement)
- Request count
- Average latency
- Error rate
- Cache hit rate

---

**This architecture provides a simple yet powerful TTS solution that balances ease of use with production-ready features.**
