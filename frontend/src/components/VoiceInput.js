import React, { useState, useEffect } from 'react';
import './VoiceInput.css';

const VoiceInput = ({ onTranscript }) => {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [recognition, setRecognition] = useState(null);

    useEffect(() => {
        // Check if browser supports speech recognition
        if ('webkitSpeechRecognition' in window) {
            const recognition = new window.webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;

            recognition.onstart = () => {
                setIsListening(true);
            };

            recognition.onresult = (event) => {
                const current = event.resultIndex;
                const transcript = event.results[current][0].transcript;
                setTranscript(transcript);
                onTranscript(transcript);
            };

            recognition.onend = () => {
                setIsListening(false);
            };

            recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                setIsListening(false);
            };

            setRecognition(recognition);
        }
    }, [onTranscript]);

    const startListening = () => {
        if (recognition) {
            recognition.start();
        }
    };

    const stopListening = () => {
        if (recognition) {
            recognition.stop();
        }
    };

    return (
        <div className="voice-input">
            {recognition ? (
                <>
                    <button
                        className={`mic-button ${isListening ? 'active' : ''}`}
                        onClick={isListening ? stopListening : startListening}
                    >
                        {isListening ? 'Stop' : 'Start'} Voice Input
                    </button>
                    {isListening && <div className="listening-indicator">Listening...</div>}
                    {transcript && <div className="transcript">{transcript}</div>}
                </>
            ) : (
                <div className="error-message">
                    Speech recognition is not supported in your browser.
                </div>
            )}
        </div>
    );
};

export default VoiceInput;