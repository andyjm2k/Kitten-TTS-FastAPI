# 🐱 Kitten TTS - Modern WebUI + OpenAI Compatible API

A high-quality, lightweight text-to-speech solution powered by [KittenTTS](https://huggingface.co/KittenML/kitten-tts-mini-0.8) with a beautiful web interface and OpenAI-compatible API.

## ✨ Features

- **🎯 OpenAI-Compatible API**: Drop-in replacement for OpenAI's TTS API
- **🌐 Modern WebUI**: Beautiful, responsive web interface
- **🔒 API Key Authentication**: Optional security for production use
- **🐳 Docker Ready**: Easy deployment with Docker Compose
- **⚡ Lightweight**: Only ~79MB model size, works on CPU
- **🎙️ Multiple Voices**: 8 different voice options
- **📦 Multiple Formats**: MP3, WAV, Opus, FLAC support

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

#### Without API Key (Development)

```bash
docker-compose up -d
```

#### With API Key (Production)

```bash
# Set your API key
export API_KEY="your-secret-api-key"

# Start with authentication
docker-compose -f docker-compose.api-key.yml up -d
```

Access the WebUI at: http://localhost:8000

### Option 2: Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install KittenTTS
pip install https://github.com/KittenML/KittenTTS/releases/download/0.8/kittentts-0.8.0-py3-none-any.whl

# Run the server
python app.py
```

## 🔧 Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `MODEL_NAME` | `KittenML/kitten-tts-mini-0.8` | Model to use |
| `API_KEY` | (empty) | API key for authentication (optional) |

## 📖 API Usage

### OpenAI-Compatible Endpoints

#### Generate Speech

```bash
curl http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "kitten-tts-mini-0.8",
    "input": "Hello, this is a test!",
    "voice": "Jasper",
    "response_format": "mp3"
  }' \
  --output speech.mp3
```

**Voices:** `Bella`, `Jasper`, `Luna`, `Bruno`, `Rosie`, `Hugo`, `Kiki`, `Leo`

**Formats:** `mp3`, `wav`, `opus`, `flac`

**OpenAI Voice Mapping:**
- `alloy` → Jasper
- `echo` → Bruno
- `fable` → Bella
- `onyx` → Hugo
- `nova` → Luna
- `shimmer` → Rosie

#### List Voices

```bash
curl http://localhost:8000/v1/audio/voices \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### List Models

```bash
curl http://localhost:8000/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Python Example

```python
import requests

# Without API key
response = requests.post(
    "http://localhost:8000/v1/audio/speech",
    json={
        "model": "kitten-tts-mini-0.8",
        "input": "Hello world!",
        "voice": "Jasper",
        "response_format": "mp3"
    }
)

# With API key
headers = {"Authorization": "Bearer YOUR_API_KEY"}
response = requests.post(
    "http://localhost:8000/v1/audio/speech",
    headers=headers,
    json={
        "model": "kitten-tts-mini-0.8",
        "input": "Hello world!",
        "voice": "Jasper",
        "response_format": "mp3"
    }
)

# Save audio
with open("speech.mp3", "wb") as f:
    f.write(response.content)
```

### JavaScript Example

```javascript
const response = await fetch('http://localhost:8000/v1/audio/speech', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    model: 'kitten-tts-mini-0.8',
    input: 'Hello world!',
    voice: 'Jasper',
    response_format: 'mp3'
  })
});

const blob = await response.blob();
const url = URL.createObjectURL(blob);
const audio = new Audio(url);
audio.play();
```

## 🐳 Publishing Docker Image

### Step 1: Build the Docker Image

```bash
# Build locally first to test
docker build -t kitten-tts:latest .
```

### Step 2: Login to Docker Hub

```bash
# Login to Docker Hub
docker login

# Or login to GitHub Container Registry
docker login ghcr.io

# Or login to Google Container Registry
gcloud auth configure-docker
```

### Step 3: Tag the Image

```bash
# For Docker Hub
docker tag kitten-tts:latest your-username/kitten-tts:latest
docker tag kitten-tts:latest your-username/kitten-tts:0.8.0

# For GitHub Container Registry
docker tag kitten-tts:latest ghcr.io/your-username/kitten-tts:latest
docker tag kitten-tts:latest ghcr.io/your-username/kitten-tts:0.8.0

# For Google Container Registry
docker tag kitten-tts:latest gcr.io/your-project/kitten-tts:latest
```

### Step 4: Push the Image

```bash
# Push to Docker Hub
docker push your-username/kitten-tts:latest
docker push your-username/kitten-tts:0.8.0

# Push to GitHub Container Registry
docker push ghcr.io/your-username/kitten-tts:latest
docker push ghcr.io/your-username/kitten-tts:0.8.0

# Push to Google Container Registry
docker push gcr.io/your-project/kitten-tts:latest
```

### Step 5: Multi-Architecture Build (Optional)

For supporting multiple architectures (amd64, arm64):

```bash
# Install buildx if not already installed
docker buildx create --use

# Build and push multi-arch image
docker buildx build --platform linux/amd64,linux/arm64 \
  -t your-username/kitten-tts:latest \
  -t your-username/kitten-tts:0.8.0 \
  --push .
```

### Step 6: Using Published Image

```bash
# Pull and run
docker run -p 8000:8000 your-username/kitten-tts:latest

# Or with Docker Compose
# Update docker-compose.yml image field:
# image: your-username/kitten-tts:latest
```

## 📁 Project Structure

```
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker build configuration
├── docker-compose.yml    # Docker Compose (no auth)
├── docker-compose.api-key.yml  # Docker Compose (with auth)
├── static/
│   └── index.html        # WebUI
└── README.md             # This file
```

## 🔒 Security Considerations

1. **API Key**: Always set `API_KEY` in production environments
2. **HTTPS**: Use a reverse proxy (nginx, traefik) for HTTPS in production
3. **Rate Limiting**: Implement rate limiting for public deployments
4. **Network**: Don't expose the container directly to the internet

Example nginx configuration:

```nginx
server {
    listen 443 ssl;
    server_name tts.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🎯 Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## 📊 Model Information

- **Model**: KittenTTS Mini 0.8
- **Parameters**: 80 million
- **Size**: ~79MB
- **Architecture**: StyleTTS 2
- **Sample Rate**: 24kHz
- **GPU Required**: No (works on CPU)

## 🤝 Acknowledgements

- [KittenML](https://huggingface.co/KittenML) for the amazing TTS model
- [StyleTTS 2](https://github.com/yl4579/StyleTTS2) architecture

## 📄 License

This project follows the license of the underlying KittenTTS model. Please check the [original repository](https://huggingface.co/KittenML/kitten-tts-mini-0.8) for licensing details.

## 🐛 Troubleshooting

### Model Download Issues

If the model fails to download on first run, ensure you have internet connectivity. The model will be cached in the Docker volume for subsequent runs.

### Memory Issues

The model requires approximately 500MB-1GB of RAM. Ensure your container has sufficient memory allocated.

### Audio Quality Issues

Try different voices to find the best match for your use case. Each voice has unique characteristics.

## 📞 Support

For issues related to the KittenTTS model itself, please refer to the [official repository](https://huggingface.co/KittenML/kitten-tts-mini-0.8).

For issues with this wrapper/API, please open an issue on the project repository.
