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

## 🚀 Quick Start - Choose Your Method

### Method 1: Docker Compose (Recommended) ⭐

The easiest and most consistent way to run Kitten TTS.

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

**Access the WebUI:** http://localhost:8000

**View logs:** `docker-compose logs -f`  
**Stop:** `docker-compose down`

---

### Method 2: Startup Script (Smart Auto-Detect) 🤖

The `start.sh` script automatically detects if Docker is available and chooses the best method.

```bash
# Make executable (first time only)
chmod +x start.sh

# Run the script
./start.sh
```

**What it does:**
- If Docker is available → Uses Docker Compose
- If Docker is not available → Sets up Python virtual environment and runs locally
- Automatically creates `.env` file if missing
- Handles API key configuration

**Access the WebUI:** http://localhost:8000

---

### Method 3: Direct Python Execution 🐍

Run directly with Python without Docker.

```bash
# Install dependencies
pip install -r requirements.txt

# Install KittenTTS
pip install https://github.com/KittenML/KittenTTS/releases/download/0.8/kittentts-0.8.0-py3-none-any.whl

# Run the server
python app.py
```

**With API Key:**
```bash
export API_KEY="your-secret-key"
python app.py
```

**Access the WebUI:** http://localhost:8000

**Stop:** Press `Ctrl+C`

---

### Method 4: Web UI Only (Static Files) 🌐

If you just want to serve the WebUI and connect to a remote Kitten TTS API:

```bash
# Using Python's built-in HTTP server
cd static
python -m http.server 3000

# Or using Node.js http-server
npm install -g http-server
cd static
http-server -p 3000
```

Then edit `static/index.html` to change the API endpoint from `/v1/audio/speech` to your remote server URL (e.g., `https://tts.yourdomain.com/v1/audio/speech`).

**Access the WebUI:** http://localhost:3000

---

## 🔧 Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `MODEL_NAME` | `KittenML/kitten-tts-mini-0.8` | Model to use |
| `API_KEY` | (empty) | API key for authentication (optional) |

### Using Configuration

**Via `.env` file:**
```bash
cp .env.example .env
# Edit .env with your settings
```

**Via environment variables:**
```bash
export API_KEY="my-secret-key"
export PORT=8000
```

**Via Docker Compose:**
```yaml
environment:
  - API_KEY=my-secret-key
  - PORT=8000
```

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

## 📁 Project Structure

```
kitten-tts/
├── app.py                      # Main FastAPI application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker build configuration
├── docker-compose.yml          # Docker Compose (no auth)
├── docker-compose.api-key.yml  # Docker Compose (with auth)
├── start.sh                    # Smart startup script
├── .env.example                # Environment template
├── .dockerignore               # Docker ignore patterns
│
├── static/
│   └── index.html              # WebUI
│
├── examples/
│   ├── usage_examples.py       # Python examples
│   └── usage_examples.js       # JavaScript examples
│
├── test_api.py                 # API test suite
│
├── README.md               # This file
├── QUICKSTART.md           # 5-minute quick start
├── PUBLISHING_GUIDE.md     # Docker publishing guide
├── ARCHITECTURE.md         # System architecture
└── PROJECT_SUMMARY.md      # Project overview
```

## 🔒 Security Considerations

1. **API Key**: Always set `API_KEY` in production environments
2. **HTTPS**: Use a reverse proxy (nginx, traefik) for HTTPS in production
3. **Rate Limiting**: Implement rate limiting for public deployments
4. **Network**: Don't expose the container directly to the internet

### Example nginx Configuration

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
        
        # Rate limiting
        limit_req zone=one burst=10 nodelay;
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

If the model fails to download on first run:
- Ensure you have internet connectivity
- The model will be cached in the Docker volume for subsequent runs
- Manual cache location: `/root/.cache/huggingface`

### Memory Issues

The model requires approximately 500MB-1GB of RAM:
```bash
# Increase container memory
docker update --memory 2g kitten-tts
```

### Port Already in Use

```bash
# Find what's using port 8000
lsof -i :8000

# Change port in .env
PORT=8001
```

### Audio Quality Issues

- Try different voices to find the best match
- Ensure your audio player supports the output format
- Try WAV format for highest quality

### Rebuilding Docker Image After Changes

If you modify code and need to rebuild:
```bash
# Stop current container
docker-compose down

# Rebuild image
docker-compose build --no-cache

# Start updated service
docker-compose up -d

# View logs to verify
docker-compose logs -f
```

## 📞 Support

- **Model Issues**: [KittenTTS HuggingFace](https://huggingface.co/KittenML/kitten-tts-mini-0.8)
- **API/Deployment Issues**: See documentation in this repository
- **Examples**: Check `examples/` folder for usage code

## 📚 Additional Documentation

| Document | Purpose |
|----------|---------|
| [`QUICKSTART.md`](QUICKSTART.md) | Get started in 5 minutes |
| [`PUBLISHING_GUIDE.md`](PUBLISHING_GUIDE.md) | Publish Docker images to registries |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | System architecture and design |
| [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md) | Complete project overview |
| [`examples/`](examples/) | Code examples in Python and JavaScript |

---

**Happy Text-to-Speech! 🐱🎵**
