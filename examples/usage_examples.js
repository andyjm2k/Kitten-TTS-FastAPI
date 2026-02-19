/**
 * Kitten TTS API - JavaScript Usage Examples
 * 
 * Run with: node usage_examples.js
 */

const fs = require('fs');
const path = require('path');

// Configuration
const BASE_URL = process.env.KITTEN_BASE_URL || 'http://localhost:8000';
const API_KEY = process.env.KITTEN_API_KEY || '';

/**
 * Get headers with optional API key
 */
function getHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    if (API_KEY) {
        headers['Authorization'] = `Bearer ${API_KEY}`;
    }
    return headers;
}

/**
 * Example 1: Basic Text-to-Speech
 */
async function exampleBasicTTS() {
    console.log('Example 1: Basic TTS');
    console.log('-'.repeat(40));
    
    try {
        const response = await fetch(`${BASE_URL}/v1/audio/speech`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({
                model: 'kitten-tts-mini-0.8',
                input: 'Hello! This is a basic text-to-speech example.',
                voice: 'Jasper',
                response_format: 'mp3'
            })
        });
        
        if (response.ok) {
            const buffer = Buffer.from(await response.arrayBuffer());
            fs.writeFileSync('output_basic.mp3', buffer);
            console.log('✓ Audio saved to output_basic.mp3');
        } else {
            const error = await response.json();
            console.log(`✗ Error: ${response.status} - ${error.detail}`);
        }
    } catch (error) {
        console.log(`✗ Error: ${error.message}`);
    }
    
    console.log();
}

/**
 * Example 2: Different Voices
 */
async function exampleDifferentVoices() {
    console.log('Example 2: Different Voices');
    console.log('-'.repeat(40));
    
    const voices = ['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo'];
    const text = 'This is a voice demonstration.';
    
    for (const voice of voices) {
        console.log(`Generating with voice: ${voice}`);
        
        try {
            const response = await fetch(`${BASE_URL}/v1/audio/speech`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify({
                    model: 'kitten-tts-mini-0.8',
                    input: text,
                    voice: voice,
                    response_format: 'mp3'
                })
            });
            
            if (response.ok) {
                const buffer = Buffer.from(await response.arrayBuffer());
                const filename = `output_voice_${voice.toLowerCase()}.mp3`;
                fs.writeFileSync(filename, buffer);
                console.log(`  ✓ Saved: ${filename}`);
            } else {
                console.log(`  ✗ Error: ${response.status}`);
            }
        } catch (error) {
            console.log(`  ✗ Error: ${error.message}`);
        }
    }
    
    console.log();
}

/**
 * Example 3: List Available Voices
 */
async function exampleListVoices() {
    console.log('Example 3: List Available Voices');
    console.log('-'.repeat(40));
    
    try {
        const response = await fetch(`${BASE_URL}/v1/audio/voices`, {
            headers: getHeaders()
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log(`Available voices (${data.data.length}):`);
            data.data.forEach(voice => {
                console.log(`  - ${voice.name} (ID: ${voice.id})`);
            });
        } else {
            console.log(`✗ Error: ${response.status}`);
        }
    } catch (error) {
        console.log(`✗ Error: ${error.message}`);
    }
    
    console.log();
}

/**
 * Example 4: OpenAI-Compatible Usage
 */
async function exampleOpenAICompatibility() {
    console.log('Example 4: OpenAI Voice Compatibility');
    console.log('-'.repeat(40));
    
    const openai_voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'];
    const text = 'This uses OpenAI-compatible voice names.';
    
    for (const openai_voice of openai_voices) {
        console.log(`Using OpenAI voice: ${openai_voice}`);
        
        try {
            const response = await fetch(`${BASE_URL}/v1/audio/speech`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify({
                    model: 'kitten-tts-mini-0.8',
                    input: text,
                    voice: openai_voice,
                    response_format: 'mp3'
                })
            });
            
            if (response.ok) {
                const buffer = Buffer.from(await response.arrayBuffer());
                const filename = `output_openai_${openai_voice}.mp3`;
                fs.writeFileSync(filename, buffer);
                console.log(`  ✓ Saved: ${filename}`);
            } else {
                console.log(`  ✗ Error: ${response.status}`);
            }
        } catch (error) {
            console.log(`  ✗ Error: ${error.message}`);
        }
    }
    
    console.log();
}

/**
 * Example 5: Play Audio in Browser (Frontend Example)
 */
function exampleFrontendUsage() {
    console.log('Example 5: Frontend/Browser Usage');
    console.log('-'.repeat(40));
    console.log(`
HTML Example:
-------------
<button onclick="generateSpeech()">Generate Speech</button>
<audio id="audioPlayer" controls></audio>

<script>
async function generateSpeech() {
    const response = await fetch('http://localhost:8000/v1/audio/speech', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // 'Authorization': 'Bearer YOUR_API_KEY' // if enabled
        },
        body: JSON.stringify({
            model: 'kitten-tts-mini-0.8',
            input: 'Hello from the browser!',
            voice: 'Jasper',
            response_format: 'mp3'
        })
    });
    
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    document.getElementById('audioPlayer').src = url;
    document.getElementById('audioPlayer').play();
}
<\/script>
    `);
    console.log();
}

/**
 * Example 6: Health Check
 */
async function exampleHealthCheck() {
    console.log('Example 6: Health Check');
    console.log('-'.repeat(40));
    
    try {
        const response = await fetch(`${BASE_URL}/health`);
        
        if (response.ok) {
            const data = await response.json();
            console.log(`Status: ${data.status}`);
            console.log(`Model loaded: ${data.model_loaded}`);
        } else {
            console.log(`✗ Error: ${response.status}`);
        }
    } catch (error) {
        console.log(`✗ Error: ${error.message}`);
    }
    
    console.log();
}

/**
 * Example 7: Batch Processing
 */
async function exampleBatchProcessing() {
    console.log('Example 7: Batch Processing');
    console.log('-'.repeat(40));
    
    const texts = [
        'Welcome to our application!',
        'Your order has been confirmed.',
        'Thank you for using our service.',
        'Have a great day!'
    ];
    
    console.log(`Processing ${texts.length} texts...`);
    
    for (let i = 0; i < texts.length; i++) {
        const text = texts[i];
        console.log(`  [${i + 1}/${texts.length}] Processing: '${text.substring(0, 30)}...'`);
        
        try {
            const response = await fetch(`${BASE_URL}/v1/audio/speech`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify({
                    model: 'kitten-tts-mini-0.8',
                    input: text,
                    voice: 'Bella',
                    response_format: 'mp3'
                })
            });
            
            if (response.ok) {
                const buffer = Buffer.from(await response.arrayBuffer());
                const filename = `output_batch_${(i + 1).toString().padStart(2, '0')}.mp3`;
                fs.writeFileSync(filename, buffer);
                console.log(`    ✓ Saved: ${filename}`);
            } else {
                console.log(`    ✗ Error: ${response.status}`);
            }
        } catch (error) {
            console.log(`    ✗ Error: ${error.message}`);
        }
    }
    
    console.log();
}

/**
 * Main - Run All Examples
 */
async function main() {
    console.log('='.repeat(60));
    console.log('Kitten TTS API - JavaScript Usage Examples');
    console.log('='.repeat(60));
    console.log(`Base URL: ${BASE_URL}`);
    console.log(`API Key: ${API_KEY ? 'Set' : 'Not set'}`);
    console.log('='.repeat(60));
    console.log();
    
    const examples = [
        exampleHealthCheck,
        exampleListVoices,
        exampleBasicTTS,
        exampleDifferentVoices,
        exampleOpenAICompatibility,
        exampleFrontendUsage,
        exampleBatchProcessing
    ];
    
    for (const example of examples) {
        try {
            await example();
        } catch (error) {
            console.log(`✗ Example failed: ${error.message}`);
            console.log();
        }
    }
    
    console.log('='.repeat(60));
    console.log('All examples completed!');
    console.log('='.repeat(60));
}

// Run if executed directly
if (require.main === module) {
    main().catch(console.error);
}

module.exports = {
    getHeaders,
    exampleBasicTTS,
    exampleDifferentVoices,
    exampleListVoices,
    exampleOpenAICompatibility,
    exampleHealthCheck,
    exampleBatchProcessing
};
