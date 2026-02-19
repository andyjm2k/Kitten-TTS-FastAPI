"""
Kitten TTS API - Usage Examples

This file demonstrates various ways to use the Kitten TTS API.
"""

import requests
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = os.getenv("KITTEN_API_KEY", "")  # Optional

def get_headers():
    """Get headers with optional API key"""
    headers = {}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    return headers


# ============================================================================
# Example 1: Basic Text-to-Speech
# ============================================================================

def example_basic_tts():
    """Generate speech with default settings"""
    print("Example 1: Basic TTS")
    print("-" * 40)
    
    response = requests.post(
        f"{BASE_URL}/v1/audio/speech",
        headers=get_headers(),
        json={
            "model": "kitten-tts-mini-0.8",
            "input": "Hello! This is a basic text-to-speech example.",
            "voice": "Jasper",
            "response_format": "mp3"
        }
    )
    
    if response.status_code == 200:
        with open("output_basic.mp3", "wb") as f:
            f.write(response.content)
        print("✓ Audio saved to output_basic.mp3")
    else:
        print(f"✗ Error: {response.status_code} - {response.text}")
    
    print()


# ============================================================================
# Example 2: Different Voices
# ============================================================================

def example_different_voices():
    """Generate speech with different voices"""
    print("Example 2: Different Voices")
    print("-" * 40)
    
    voices = ["Bella", "Jasper", "Luna", "Bruno", "Rosie", "Hugo", "Kiki", "Leo"]
    text = "This is a voice demonstration."
    
    for voice in voices:
        print(f"Generating with voice: {voice}")
        
        response = requests.post(
            f"{BASE_URL}/v1/audio/speech",
            headers=get_headers(),
            json={
                "model": "kitten-tts-mini-0.8",
                "input": text,
                "voice": voice,
                "response_format": "mp3"
            }
        )
        
        if response.status_code == 200:
            filename = f"output_voice_{voice.lower()}.mp3"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"  ✓ Saved: {filename}")
        else:
            print(f"  ✗ Error: {response.status_code}")
    
    print()


# ============================================================================
# Example 3: Different Audio Formats
# ============================================================================

def example_different_formats():
    """Generate speech in different audio formats"""
    print("Example 3: Different Audio Formats")
    print("-" * 40)
    
    formats = ["mp3", "wav", "opus", "flac"]
    text = "This demonstrates different audio formats."
    
    for fmt in formats:
        print(f"Generating {fmt.upper()} format...")
        
        response = requests.post(
            f"{BASE_URL}/v1/audio/speech",
            headers=get_headers(),
            json={
                "model": "kitten-tts-mini-0.8",
                "input": text,
                "voice": "Jasper",
                "response_format": fmt
            }
        )
        
        if response.status_code == 200:
            filename = f"output_format.{fmt}"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"  ✓ Saved: {filename} ({len(response.content)} bytes)")
        else:
            print(f"  ✗ Error: {response.status_code}")
    
    print()


# ============================================================================
# Example 4: OpenAI Voice Compatibility
# ============================================================================

def example_openai_compatibility():
    """Use OpenAI-style voice names (automatically mapped)"""
    print("Example 4: OpenAI Voice Compatibility")
    print("-" * 40)
    
    # These OpenAI voice names are automatically mapped to KittenTTS voices
    openai_voices = {
        "alloy": "Jasper",
        "echo": "Bruno",
        "fable": "Bella",
        "onyx": "Hugo",
        "nova": "Luna",
        "shimmer": "Rosie"
    }
    
    text = "This uses OpenAI-compatible voice names."
    
    for openai_voice, kitten_voice in openai_voices.items():
        print(f"Using OpenAI voice '{openai_voice}' (mapped to {kitten_voice})...")
        
        response = requests.post(
            f"{BASE_URL}/v1/audio/speech",
            headers=get_headers(),
            json={
                "model": "kitten-tts-mini-0.8",
                "input": text,
                "voice": openai_voice,
                "response_format": "mp3"
            }
        )
        
        if response.status_code == 200:
            filename = f"output_openai_{openai_voice}.mp3"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"  ✓ Saved: {filename}")
        else:
            print(f"  ✗ Error: {response.status_code}")
    
    print()


# ============================================================================
# Example 5: List Available Voices
# ============================================================================

def example_list_voices():
    """Get list of available voices"""
    print("Example 5: List Available Voices")
    print("-" * 40)
    
    response = requests.get(
        f"{BASE_URL}/v1/audio/voices",
        headers=get_headers()
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Available voices ({len(data['data'])}):")
        for voice in data['data']:
            print(f"  - {voice['name']} (ID: {voice['id']})")
    else:
        print(f"✗ Error: {response.status_code}")
    
    print()


# ============================================================================
# Example 6: List Available Models
# ============================================================================

def example_list_models():
    """Get list of available models"""
    print("Example 6: List Available Models")
    print("-" * 40)
    
    response = requests.get(
        f"{BASE_URL}/v1/models",
        headers=get_headers()
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Available models ({len(data['data'])}):")
        for model in data['data']:
            print(f"  - {model['id']}")
    else:
        print(f"✗ Error: {response.status_code}")
    
    print()


# ============================================================================
# Example 7: Health Check
# ============================================================================

def example_health_check():
    """Check server health"""
    print("Example 7: Health Check")
    print("-" * 40)
    
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Model loaded: {data['model_loaded']}")
    else:
        print(f"✗ Error: {response.status_code}")
    
    print()


# ============================================================================
# Example 8: Batch Processing
# ============================================================================

def example_batch_processing():
    """Process multiple texts in batch"""
    print("Example 8: Batch Processing")
    print("-" * 40)
    
    texts = [
        "Welcome to our application!",
        "Your order has been confirmed.",
        "Thank you for using our service.",
        "Have a great day!"
    ]
    
    print(f"Processing {len(texts)} texts...")
    
    for i, text in enumerate(texts, 1):
        print(f"  [{i}/{len(texts)}] Processing: '{text[:30]}...'")
        
        response = requests.post(
            f"{BASE_URL}/v1/audio/speech",
            headers=get_headers(),
            json={
                "model": "kitten-tts-mini-0.8",
                "input": text,
                "voice": "Bella",
                "response_format": "mp3"
            }
        )
        
        if response.status_code == 200:
            filename = f"output_batch_{i:02d}.mp3"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"    ✓ Saved: {filename}")
        else:
            print(f"    ✗ Error: {response.status_code}")
    
    print()


# ============================================================================
# Example 9: Streaming-like Processing (with progress)
# ============================================================================

def example_long_text():
    """Process longer text with progress indication"""
    print("Example 9: Long Text Processing")
    print("-" * 40)
    
    long_text = """
    Artificial intelligence is transforming the way we live and work. 
    From healthcare to education, from transportation to entertainment, 
    AI technologies are creating new opportunities and solving complex problems. 
    The future of AI is bright, with endless possibilities for innovation 
    and improvement in human life.
    """
    
    print(f"Processing {len(long_text)} characters...")
    
    response = requests.post(
        f"{BASE_URL}/v1/audio/speech",
        headers=get_headers(),
        json={
            "model": "kitten-tts-mini-0.8",
            "input": long_text.strip(),
            "voice": "Luna",
            "response_format": "mp3"
        }
    )
    
    if response.status_code == 200:
        filename = "output_long_text.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✓ Saved: {filename} ({len(response.content)} bytes)")
        
        # Estimate duration (rough estimate: 150 words per minute)
        words = len(long_text.split())
        duration_seconds = (words / 150) * 60
        print(f"  Estimated duration: ~{duration_seconds:.1f} seconds")
    else:
        print(f"✗ Error: {response.status_code}")
    
    print()


# ============================================================================
# Example 10: Error Handling
# ============================================================================

def example_error_handling():
    """Demonstrate proper error handling"""
    print("Example 10: Error Handling")
    print("-" * 40)
    
    test_cases = [
        {"text": "", "desc": "Empty text"},
        {"text": "Valid text", "voice": "InvalidVoice", "desc": "Invalid voice"},
        {"text": "Valid text", "format": "invalid_fmt", "desc": "Invalid format"},
    ]
    
    for case in test_cases:
        print(f"Testing: {case['desc']}")
        
        payload = {
            "model": "kitten-tts-mini-0.8",
            "input": case.get("text", "Test"),
            "voice": case.get("voice", "Jasper"),
            "response_format": case.get("format", "mp3")
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/v1/audio/speech",
                headers=get_headers(),
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"  ✓ Success")
            else:
                print(f"  ⚠ Status {response.status_code}: {response.json().get('detail', 'Unknown error')}")
                
        except requests.exceptions.Timeout:
            print(f"  ✗ Timeout")
        except requests.exceptions.ConnectionError:
            print(f"  ✗ Connection error - Is the server running?")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
    
    print()


# ============================================================================
# Main - Run All Examples
# ============================================================================

def main():
    """Run all examples"""
    print("=" * 60)
    print("Kitten TTS API - Usage Examples")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"API Key: {'Set' if API_KEY else 'Not set'}")
    print("=" * 60)
    print()
    
    examples = [
        example_health_check,
        example_list_voices,
        example_list_models,
        example_basic_tts,
        example_different_voices,
        example_different_formats,
        example_openai_compatibility,
        example_batch_processing,
        example_long_text,
        example_error_handling,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"✗ Example failed: {e}")
            print()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
