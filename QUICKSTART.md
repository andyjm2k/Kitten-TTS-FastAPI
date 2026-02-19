# 🚀 Kitten TTS - Quick Start Guide

Get up and running in 5 minutes!

## Option 1: Docker (Fastest) ⚡

```bash
# Clone or download the project
cd kitten-tts

# Start with Docker Compose
docker-compose up -d

# Access WebUI
open http://localhost:8000
```

**That's it!** 🎉

---

## Option 2: Python (No Docker) 🐍

```bash
# Install dependencies
pip install -r requirements.txt

# Install KittenTTS
pip install https://github.com/KittenML/KittenTTS/releases/download/0.8/kittentts-0.8.0-py3-none-any.whl

# Run server
python app.py

# Access WebUI
open http://localhost:8000
```

---

## 📖 Basic Usage

### Web Interface

1. Open http://localhost:8000
2. Enter your text
3. Select a voice
4. Click "Generate Speech"
5. Listen or download!

### API (cURL)

```bash
# Generate speech
curl http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kitten-tts-mini-0.8",
    "input": "Hello world!",
    "voice": "Jasper",
    "response_format": "mp3"
  }' \
  --output hello.mp3

# Play it
afplay hello.mp3  # macOS
xdg-open hello.mp3  # Linux
start hello.mp3  # Windows
```

### API (Python)

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/audio/speech",
    json={
        "model": "kitten-tts-mini-0.8",
        "input": "Hello world!",
        "voice": "Jasper",
        "response_format": "mp3"
    }
)

with open("hello.mp3", "wb") as f:
    f.write(response.content)
```

### API (JavaScript)

```javascript
const response = await fetch('http://localhost:8000/v1/audio/speech', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'kitten-tts-mini-0.8',
    input: 'Hello world!',
    voice: 'Jasper',
    response_format: 'mp3'
  })
});

const blob = await response.blob();
const audio = new Audio(URL.createObjectURL(blob));
audio.play();
```

---

## 🎙️ Available Voices

| Voice | Description |
|-------|-------------|
| Bella | Female, warm |
| Jasper | Male, clear |
| Luna | Female, soft |
| Bruno | Male, deep |
| Rosie | Female, friendly |
| Hugo | Male, professional |
| Kiki | Female, energetic |
| Leo | Male, casual |

---

## 🔒 Enable API Key (Optional)

```bash
# Create .env file
echo "API_KEY=your-secret-key" > .env

# Restart with authentication
docker-compose down
docker-compose -f docker-compose.api-key.yml up -d

# Use API key in requests
curl http://localhost:8000/v1/audio/speech \
  -H "Authorization: Bearer your-secret-key" \
  ...
```

---

## 🛑 Stop Server

```bash
# Docker
docker-compose down

# Python
# Press Ctrl+C
```

---

## 📊 Check Status

```bash
# Health check
curl http://localhost:8000/health

# View logs
docker-compose logs -f
```

---

## 🎯 Next Steps

- 📖 Read the full [README.md](README.md)
- 💻 Try the [examples](examples/)
- 🐳 Learn to [publish Docker images](PUBLISHING_GUIDE.md)
- 🔧 Customize configuration in `.env`

---

## ❓ Troubleshooting

**Server won't start?**
```bash
docker-compose logs
```

**Model download fails?**
- Check internet connection
- First run downloads ~79MB model

**Port already in use?**
```bash
# Change port in .env
PORT=8001
```

**Need help?**
- Check [README.md](README.md) for detailed docs
- Review [examples](examples/) for code samples

---

**Enjoy! 🐱🎵**
