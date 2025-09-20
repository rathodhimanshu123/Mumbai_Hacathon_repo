Sure, here's the contents for the file /ai-nurse-companion/ai-nurse-companion/frontend/src/components/Chat.js:

import React, { useState, useEffect, useRef } from 'react';
import VoiceInput from './VoiceInput';
import './Chat.css';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [healthData, setHealthData] = useState(null);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
        fetchHealthData();
    }, [messages]);

    const fetchHealthData = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/health_data/7');
            const data = await response.json();
            setHealthData(data.health_data);
        } catch (error) {
            console.error('Error fetching health data:', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = { type: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            // Add health data context if available
            const context = healthData ? {
                recent_activity: healthData[0]
            } : {};

            // Analyze symptoms
            const response = await fetch('http://localhost:8000/api/analyze_symptoms', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    symptoms: [input],
                    context: context
                }),
            });

            const data = await response.json();

            // Format the response
            const analysis = [
                `Urgency Level: ${data.urgency_level}`,
                `\nAssessment: ${data.initial_assessment}`,
                '\nRecommended Actions:',
                ...data.recommended_actions.map(action => `- ${action}`),
                '\nLifestyle Recommendations:',
                ...data.lifestyle_recommendations.map(rec => `- ${rec}`),
                '\nWarning Signs to Watch For:',
                ...data.warning_signs.map(sign => `- ${sign}`)
            ].join('\n');

            setMessages(prev => [...prev, { type: 'assistant', content: analysis }]);

            // Generate follow-up questions
            const followUpResponse = await fetch('http://localhost:8000/api/generate_followup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    conversation_history: [
                        { user: input, assistant: analysis }
                    ]
                }),
            });

            const followUpData = await followUpResponse.json();
            if (followUpData.questions) {
                setMessages(prev => [...prev, { 
                    type: 'assistant', 
                    content: 'Follow-up questions:\n' + followUpData.questions.join('\n') 
                }]);
            }
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, { 
                type: 'error', 
                content: 'Sorry, there was an error processing your request.' 
            }]);
        }

        setIsLoading(false);
    };

    const handleVoiceInput = (transcript) => {
        setInput(transcript);
    };

    return (
        <div className="chat-container">
            <div className="chat-messages">
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.type}`}>
                        <div className="message-content">
                            {message.content.split('\n').map((line, i) => (
                                <p key={i}>{line}</p>
                            ))}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="message assistant">
                        <div className="loading">Analyzing...</div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>
            <div className="input-container">
                <form onSubmit={handleSubmit} className="chat-input">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Describe your symptoms..."
                        disabled={isLoading}
                    />
                    <button type="submit" disabled={isLoading}>Send</button>
                </form>
                <VoiceInput onTranscript={handleVoiceInput} />
            </div>
        </div>
    );
};

export default Chat;