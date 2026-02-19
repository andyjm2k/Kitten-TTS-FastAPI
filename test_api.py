#!/usr/bin/env python3
"""
Test script for Kitten TTS API
"""

import requests
import os

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("TEST_API_KEY", "")

def get_headers():
    """Get headers with optional API key"""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    return headers

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    return response.status_code == 200

def test_voices():
    """Test voices endpoint"""
    print("Testing voices endpoint...")
    response = requests.get(f"{BASE_URL}/v1/audio/voices", headers=get_headers())
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    return response.status_code == 200

def test_models():
    """Test models endpoint"""
    print("Testing models endpoint...")
    response = requests.get(f"{BASE_URL}/v1/models", headers=get_headers())
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    return response.status_code == 200

def test_speech_generation():
    """Test speech generation"""
    print("Testing speech generation...")
    
    test_cases = [
        {"voice": "Jasper", "text": "Hello, this is a test!"},
        {"voice": "Bella", "text": "How are you today?"},
        {"voice": "Luna", "text": "This is amazing!"},
    ]
    
    for i, case in enumerate(test_cases):
        print(f"\nTest {i+1}: Voice={case['voice']}, Text='{case['text']}'")
        
        response = requests.post(
            f"{BASE_URL}/v1/audio/speech",
            headers=get_headers(),
            json={
                "model": "kitten-tts-mini-0.8",
                "input": case["text"],
                "voice": case["voice"],
                "response_format": "mp3"
            }
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            filename = f"test_output_{case['voice'].lower()}.mp3"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✓ Audio saved to {filename} ({len(response.content)} bytes)")
        else:
            print(f"✗ Error: {response.text}")
    
    print()
    return True

def test_openai_voice_mapping():
    """Test OpenAI voice name mapping"""
    print("Testing OpenAI voice mapping...")
    
    mapping_tests = [
        {"voice": "alloy", "expected": "Jasper"},
        {"voice": "echo", "expected": "Bruno"},
        {"voice": "fable", "expected": "Bella"},
    ]
    
    for test in mapping_tests:
        print(f"\nMapping: {test['voice']} -> {test['expected']}")
        
        response = requests.post(
            f"{BASE_URL}/v1/audio/speech",
            headers=get_headers(),
            json={
                "model": "kitten-tts-mini-0.8",
                "input": "Testing voice mapping",
                "voice": test["voice"],
                "response_format": "wav"
            }
        )
        
        if response.status_code == 200:
            print(f"✓ Success")
        else:
            print(f"✗ Error: {response.text}")
    
    print()
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Kitten TTS API Test Suite")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"API Key: {'Set' if API_KEY else 'Not set'}")
    print("=" * 60)
    print()
    
    tests = [
        ("Health Check", test_health),
        ("List Voices", test_voices),
        ("List Models", test_models),
        ("Speech Generation", test_speech_generation),
        ("Voice Mapping", test_openai_voice_mapping),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"✗ {name} failed with exception: {e}")
            results.append((name, False))
    
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
