Sure, here's the contents for the file /ai-nurse-companion/frontend/src/App.js:

import React from 'react';
import Chat from './components/Chat';
import VoiceInput from './components/VoiceInput';

function App() {
    return (
        <div className="App">
            <h1>AI Nurse Companion</h1>
            <Chat />
            <VoiceInput />
        </div>
    );
}

export default App;